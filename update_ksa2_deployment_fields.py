#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

DEFAULT_TARGET_DIRS = [
    "microservices/test/ksa/account",
    "microservices/test/ksa/acquiring",
    "microservices/test/ksa/market",
    "microservices/test/ksa/wallet",
]
SKIP_FILE_NAMES = {"recon-mock.yml", "recon-mock.yaml"}
DEPLOYMENT_KIND = "kind: Deployment"
DOC_SEPARATOR_RE = re.compile(r"(?m)^---\s*$")
INIT_CONTAINERS_RE = re.compile(r"(?m)^\s{6}initContainers:\s*$")
CONTAINERS_RE = re.compile(r"(?m)^\s{6}containers:\s*$")
IMAGE_PULL_POLICY_RE = re.compile(
    r"(?m)(^\s{10}imagePullPolicy:[^\n]*\n)(?!\s{10}securityContext:\n)"
)
LOGS_MOUNT_RE = re.compile(
    r"(?ms)^\s{12}- name:\s*(?P<volume>[^\n#]+)\n"
    r"\s{14}mountPath:\s*/tiqmo_logs[ \t]*"
    r"(?:\n\s{14}subPathExpr:\s*(?P<subpath>[^\n]+))?"
)
SUBPATH_SERVICE_RE = re.compile(r"\$\(POD_NAMESPACE\)/([^/\s]+)/\$\(POD_ID\)")
INIT_RANGE_RE = re.compile(r"(?ms)^\s{6}initContainers:\s*$.*?(?=^\s{6}containers:\s*$|\Z)")


def _read_text_with_fallback(path: Path) -> tuple[str, str]:
    last_error: UnicodeDecodeError | None = None
    for encoding in ("utf-8", "utf-8-sig", "gb18030", "cp936"):
        try:
            return path.read_text(encoding=encoding), encoding
        except UnicodeDecodeError as exc:
            last_error = exc

    raise RuntimeError(f"Unable to decode file: {path}") from last_error


def _split_first_document(text: str) -> tuple[str, str]:
    match = DOC_SEPARATOR_RE.search(text)
    if not match:
        return text, ""
    return text[: match.start()], text[match.start() :]


def _relative_path(repo_root: Path, file_path: Path) -> str:
    try:
        return file_path.relative_to(repo_root).as_posix()
    except ValueError:
        return file_path.as_posix()


def _build_init_block(service_name: str, logs_volume_name: str) -> str:
    return (
        "      initContainers:\n"
        "        - name: log-setup\n"
        "          image: docker.repo.swifer.co/busybox:latest\n"
        "          imagePullPolicy: IfNotPresent\n"
        "          env:\n"
        "            - name: POD_ID\n"
        "              valueFrom:\n"
        "                fieldRef:\n"
        "                  fieldPath: metadata.name\n"
        "            - name: POD_NAMESPACE\n"
        "              valueFrom:\n"
        "                fieldRef:\n"
        "                  fieldPath: metadata.namespace\n"
        "          command:\n"
        "            - sh\n"
        "            - -c\n"
        "            - |\n"
        "              LOG_BASE=\"/tiqmo_logs\"\n"
        f"              SUB_DIR=\"${{POD_NAMESPACE}}/{service_name}/${{POD_ID}}\"\n"
        "              FULL_PATH=\"${LOG_BASE}/${SUB_DIR}\"\n"
        "              mkdir -p \"${FULL_PATH}\"\n"
        "              chown -R 1001:100 \"${FULL_PATH}\"\n"
        "              echo \"Log directory ready: ${FULL_PATH}\"\n"
        "          volumeMounts:\n"
        f"            - name: {logs_volume_name}\n"
        "              mountPath: /tiqmo_logs\n"
        "          securityContext:\n"
        "            runAsUser: 0\n"
    )


def _extract_logs_setup_info(deployment_doc: str) -> tuple[str | None, str | None, str | None]:
    match = LOGS_MOUNT_RE.search(deployment_doc)
    if not match:
        return None, None, "missing_logs_mount"

    logs_volume_name = match.group("volume").strip().strip("\"'")
    subpath_expr = (match.group("subpath") or "").strip()
    if not subpath_expr:
        return None, logs_volume_name, "missing_subpath_expr"

    subpath_match = SUBPATH_SERVICE_RE.search(subpath_expr)
    if not subpath_match:
        return None, logs_volume_name, "unrecognized_subpath_expr"

    return subpath_match.group(1), logs_volume_name, None


def _insert_init_containers(
    deployment_doc: str,
    service_name: str,
    logs_volume_name: str,
) -> tuple[str, bool]:
    if INIT_CONTAINERS_RE.search(deployment_doc):
        return deployment_doc, False

    containers_match = CONTAINERS_RE.search(deployment_doc)
    if not containers_match:
        return deployment_doc, False

    init_block = _build_init_block(service_name, logs_volume_name)
    updated = (
        deployment_doc[: containers_match.start()]
        + init_block
        + deployment_doc[containers_match.start() :]
    )
    return updated, True


def _insert_container_security(deployment_doc: str) -> tuple[str, bool]:
    containers_match = CONTAINERS_RE.search(deployment_doc)
    if not containers_match:
        return deployment_doc, False

    head = deployment_doc[: containers_match.end()]
    tail = deployment_doc[containers_match.end() :]
    updated_tail, replacements = IMAGE_PULL_POLICY_RE.subn(
        "\\1          securityContext:\n            runAsUser: 1001\n",
        tail,
        count=1,
    )
    return head + updated_tail, replacements > 0


def _remove_pod_namespace_prefix_in_init(deployment_doc: str) -> tuple[str, int]:
    init_match = INIT_RANGE_RE.search(deployment_doc)
    if not init_match:
        return deployment_doc, 0

    init_section = init_match.group(0)
    updated_init_section, removed_count = re.subn(r"\$\{POD_NAMESPACE\}/", "", init_section)
    if removed_count == 0:
        return deployment_doc, 0

    updated = (
        deployment_doc[: init_match.start()]
        + updated_init_section
        + deployment_doc[init_match.end() :]
    )
    return updated, removed_count


def patch_text(
    text: str,
    file_path: Path,
    add_fields: bool,
    remove_pod_namespace_prefix: bool,
) -> tuple[str, bool, bool, int, str | None]:
    deployment_doc, remaining_docs = _split_first_document(text)
    if DEPLOYMENT_KIND not in deployment_doc:
        return text, False, False, 0, "not_deployment"

    if file_path.name in SKIP_FILE_NAMES:
        return text, False, False, 0, "special_case_recon_mock"

    changed_init = False
    changed_container = False

    if add_fields:
        if not INIT_CONTAINERS_RE.search(deployment_doc):
            service_name, logs_volume_name, skip_reason = _extract_logs_setup_info(deployment_doc)
            if skip_reason:
                return text, False, False, 0, skip_reason
            deployment_doc, changed_init = _insert_init_containers(
                deployment_doc,
                service_name=service_name,
                logs_volume_name=logs_volume_name,
            )

        deployment_doc, changed_container = _insert_container_security(deployment_doc)

    removed_namespace_prefix = 0
    if remove_pod_namespace_prefix:
        deployment_doc, removed_namespace_prefix = _remove_pod_namespace_prefix_in_init(deployment_doc)

    if not changed_init and not changed_container and removed_namespace_prefix == 0:
        return text, False, False, 0, None

    return (
        deployment_doc + remaining_docs,
        changed_init,
        changed_container,
        removed_namespace_prefix,
        None,
    )


def process(
    repo_root: Path,
    apply: bool,
    add_fields: bool,
    remove_pod_namespace_prefix: bool,
    target_dirs: list[str],
) -> None:
    files_set: set[Path] = set()
    for target_dir in target_dirs:
        files_set.update(repo_root.glob(f"{target_dir}/**/*.yml"))
        files_set.update(repo_root.glob(f"{target_dir}/**/*.yaml"))

    files = sorted(files_set)
    scanned_files = len(files)
    deployment_targets = 0
    modified_files: list[str] = []
    init_updates = 0
    container_updates = 0
    namespace_prefix_removed_total = 0
    skipped_by_reason: dict[str, list[str]] = defaultdict(list)

    for file_path in files:
        original, file_encoding = _read_text_with_fallback(file_path)
        updated, changed_init, changed_container, removed_namespace_prefix, skip_reason = patch_text(
            original,
            file_path=file_path,
            add_fields=add_fields,
            remove_pod_namespace_prefix=remove_pod_namespace_prefix,
        )

        if skip_reason == "not_deployment":
            continue

        deployment_targets += 1
        relative_path = _relative_path(repo_root, file_path)

        if skip_reason:
            skipped_by_reason[skip_reason].append(relative_path)
            continue

        if changed_init or changed_container or removed_namespace_prefix > 0:
            init_updates += int(changed_init)
            container_updates += int(changed_container)
            namespace_prefix_removed_total += removed_namespace_prefix
            modified_files.append(relative_path)
            if apply:
                file_path.write_text(updated, encoding=file_encoding)

    skipped_files = sum(len(paths) for paths in skipped_by_reason.values())
    mode = "APPLY" if apply else "DRY-RUN"

    print(f"mode={mode}")
    print(f"repo_root={repo_root.as_posix()}")
    print(f"target_dirs={','.join(target_dirs)}")
    print(f"scanned_files={scanned_files}")
    print(f"deployment_targets={deployment_targets}")
    print(f"modified_files={len(modified_files)}")
    print(f"skipped_files={skipped_files}")
    print(f"init_containers_inserted={init_updates}")
    print(f"container_security_inserted={container_updates}")
    print(f"pod_namespace_prefix_removed={namespace_prefix_removed_total}")

    if skipped_by_reason:
        print("--- skipped ---")
        for reason in sorted(skipped_by_reason):
            paths = skipped_by_reason[reason]
            print(f"[{reason}] {len(paths)}")
            for path in paths:
                print(path)

    if modified_files:
        print("--- files ---")
        for path in modified_files:
            print(path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Batch update non-frontend test/ksa Deployment YAML files by adding "
            "initContainers and container securityContext."
        )
    )
    parser.add_argument(
        "--repo-root",
        default=r"E:/海付&威富通gitlab仓库/fwallyt",
        help="fwallyt repository root path",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes to files (default is dry-run)",
    )
    parser.add_argument(
        "--skip-add-fields",
        action="store_true",
        help="Do not add initContainers and container securityContext",
    )
    parser.add_argument(
        "--remove-pod-namespace-prefix",
        action="store_true",
        help="Remove ${POD_NAMESPACE}/ from initContainers command section",
    )
    parser.add_argument(
        "--target-dir",
        action="append",
        dest="target_dirs",
        help=(
            "Target directory under repo root, can be repeated. "
            "Default targets are account/acquiring/market/wallet under microservices/test/ksa"
        ),
    )

    args = parser.parse_args()
    add_fields = not args.skip_add_fields

    if not add_fields and not args.remove_pod_namespace_prefix:
        parser.error("Nothing to do. Enable an operation.")

    process(
        Path(args.repo_root),
        apply=args.apply,
        add_fields=add_fields,
        remove_pod_namespace_prefix=args.remove_pod_namespace_prefix,
        target_dirs=args.target_dirs or DEFAULT_TARGET_DIRS,
    )


if __name__ == "__main__":
    main()
