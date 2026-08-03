from pathlib import Path
import re

ROOT = Path(r"E:\海付&威富通gitlab仓库\fwallyt\microservices\test")
TARGET_COUNTRIES = {"ksa", "ksa2"}
PATTERNS = ["**/pv_pvc.yml", "**/pv_pvc_logs.yml", "**/pv-pvc.yaml"]
UPDATE_PVC_SELECTOR = False
# 已创建并绑定的 PVC 不允许修改 spec.selector，默认只补 PV labels。


def split_docs(text: str) -> list[str]:
    docs = []
    current = []
    for line in text.splitlines(keepends=True):
        if line.strip() == "---":
            if "".join(current).strip():
                docs.append("".join(current).strip("\n"))
            current = []
        else:
            current.append(line)
    if "".join(current).strip():
        docs.append("".join(current).strip("\n"))
    return docs


def volume_from_name(name: str) -> str:
    lower_name = name.lower()
    if "staticfiles" in lower_name:
        return "staticfiles"
    if "logs" in lower_name:
        return "logs"
    return "share"


def collect_files(root: Path) -> list[Path]:
    files = []
    for pattern in PATTERNS:
        files.extend(root.glob(pattern))
    result = []
    for path in sorted(set(files)):
        relative = path.relative_to(root)
        if relative.parts[0] in TARGET_COUNTRIES:
            result.append(path)
    return result


def update_file(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    country = relative.parts[0]
    module = relative.parts[1]
    env = f"test-{country}"

    original = path.read_text(encoding="utf-8")
    docs = split_docs(original)
    new_docs = []

    for doc in docs:
        kind_match = re.search(r"^kind:\s*(\S+)\s*$", doc, re.MULTILINE)
        name_match = re.search(r"^\s*name:\s*([^\n]+)\s*$", doc, re.MULTILINE)
        if not kind_match or not name_match:
            raise RuntimeError(f"Unable to parse kind/name in {path}")

        kind = kind_match.group(1)
        name = name_match.group(1).strip().strip('"')
        volume = volume_from_name(name)

        if kind == "PersistentVolume":
            if "\n  labels:\n" not in doc:
                target = f"metadata:\n  name: {name}\n"
                replacement = (
                    f"metadata:\n"
                    f"  name: {name}\n"
                    f"  labels:\n"
                    f"    app: {module}\n"
                    f"    env: {env}\n"
                    f"    volume: {volume}\n"
                )
                if target not in doc:
                    raise RuntimeError(f"Unable to insert labels into {path} for {name}")
                doc = doc.replace(target, replacement, 1)
        elif kind == "PersistentVolumeClaim":
            if UPDATE_PVC_SELECTOR and "\n  selector:\n" not in doc:
                doc = (
                    f"{doc}\n"
                    f"  selector:\n"
                    f"    matchLabels:\n"
                    f"      app: {module}\n"
                    f"      env: {env}\n"
                    f"      volume: {volume}"
                )
        new_docs.append(doc)

    updated = "---\n" + "\n---\n".join(new_docs) + "\n"
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for path in collect_files(ROOT):
        if update_file(path, ROOT):
            changed.append(path)

    print(f"updated {len(changed)} files")
    for path in changed:
        print(path)


if __name__ == "__main__":
    main()
