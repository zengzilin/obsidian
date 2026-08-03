from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
HEADERS = ["服务名", "request.cpu", "request.memory", "limit.cpu", "limit.memory"]


def parse_resources(values_file: Path) -> dict[str, dict[str, str]]:
    resources = {
        "requests": {},
        "limits": {},
    }

    lines = values_file.read_text(encoding="utf-8").splitlines()
    resources_indent = None
    current_section = None
    section_indent = None

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))

        if resources_indent is None:
            if stripped == "resources:":
                resources_indent = indent
            continue

        if indent <= resources_indent:
            break

        if stripped == "requests:":
            current_section = "requests"
            section_indent = indent
            continue

        if stripped == "limits:":
            current_section = "limits"
            section_indent = indent
            continue

        if current_section and indent <= section_indent:
            current_section = None
            section_indent = None

        if not current_section or ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")

        if key in {"cpu", "memory"}:
            resources[current_section][key] = value

    return resources


def iter_service_values(base_dir: Path):
    for service_dir in sorted(path for path in base_dir.iterdir() if path.is_dir()):
        for name in ("values.yaml", "values.yml"):
            values_file = service_dir / name
            if values_file.exists():
                yield service_dir.name, values_file
                break


def main() -> None:
    print("\t".join(HEADERS))

    for service_name, values_file in iter_service_values(BASE_DIR):
        resources = parse_resources(values_file)
        requests = resources["requests"]
        limits = resources["limits"]

        row = [
            service_name,
            requests.get("cpu", "未配置"),
            requests.get("memory", "未配置"),
            limits.get("cpu", "未配置"),
            limits.get("memory", "未配置"),
        ]
        print("\t".join(row))


if __name__ == "__main__":
    main()
