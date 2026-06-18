from __future__ import annotations

import base64
import csv
import hashlib
import io
from pathlib import Path
import shutil
import tempfile
import tomllib
from zipfile import ZIP_DEFLATED, ZipFile


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def get_requires_for_build_wheel(config_settings=None):
    return []


def get_requires_for_build_sdist(config_settings=None):
    return []


def get_requires_for_build_editable(config_settings=None):
    return []


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    metadata_root = Path(metadata_directory)
    dist_info = _dist_info_name()
    target = metadata_root / dist_info
    target.mkdir(parents=True, exist_ok=True)
    _write_dist_info(target)
    return dist_info


def prepare_metadata_for_build_editable(metadata_directory, config_settings=None):
    return prepare_metadata_for_build_wheel(metadata_directory, config_settings)


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    wheel_root = Path(wheel_directory)
    wheel_root.mkdir(parents=True, exist_ok=True)

    name = _normalized_name()
    version = _project()["project"]["version"]
    dist_info = _dist_info_name()
    wheel_name = f"{name}-{version}-py3-none-any.whl"
    wheel_path = wheel_root / wheel_name

    entries: list[tuple[str, bytes]] = []
    for source in sorted((PROJECT_ROOT / "harness_v2").glob("*.py")):
        archive_name = f"harness_v2/{source.name}"
        entries.append((archive_name, source.read_bytes()))

    _append_dist_info(entries, dist_info)
    _write_wheel(wheel_path, dist_info, entries)
    return wheel_name


def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    wheel_root = Path(wheel_directory)
    wheel_root.mkdir(parents=True, exist_ok=True)

    name = _normalized_name()
    version = _project()["project"]["version"]
    dist_info = _dist_info_name()
    wheel_name = f"{name}-{version}-0.editable-py3-none-any.whl"
    wheel_path = wheel_root / wheel_name

    entries = [("harness_v2_editable.pth", f"{PROJECT_ROOT}\n".encode("utf-8"))]
    _append_dist_info(entries, dist_info)
    _write_wheel(wheel_path, dist_info, entries)
    return wheel_name


def _append_dist_info(entries: list[tuple[str, bytes]], dist_info: str) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        dist_info_root = Path(temp_dir) / dist_info
        dist_info_root.mkdir()
        _write_dist_info(dist_info_root)
        for source in sorted(dist_info_root.iterdir()):
            entries.append((f"{dist_info}/{source.name}", source.read_bytes()))


def _write_wheel(wheel_path: Path, dist_info: str, entries: list[tuple[str, bytes]]) -> None:
    record_path = f"{dist_info}/RECORD"
    record_rows = []
    for archive_name, content in entries:
        digest = base64.urlsafe_b64encode(hashlib.sha256(content).digest()).rstrip(b"=").decode("ascii")
        record_rows.append((archive_name, f"sha256={digest}", str(len(content))))
    record_rows.append((record_path, "", ""))

    record_buffer = io.StringIO(newline="")
    writer = csv.writer(record_buffer)
    writer.writerows(record_rows)
    entries.append((record_path, record_buffer.getvalue().encode("utf-8")))

    with ZipFile(wheel_path, "w", compression=ZIP_DEFLATED) as wheel:
        for archive_name, content in entries:
            wheel.writestr(archive_name, content)


def build_sdist(sdist_directory, config_settings=None):
    sdist_root = Path(sdist_directory)
    sdist_root.mkdir(parents=True, exist_ok=True)
    name = _normalized_name()
    version = _project()["project"]["version"]
    base_name = f"{name}-{version}"
    archive = shutil.make_archive(str(sdist_root / base_name), "gztar", root_dir=PROJECT_ROOT)
    return Path(archive).name


def _project() -> dict:
    with (PROJECT_ROOT / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)


def _normalized_name() -> str:
    return _project()["project"]["name"].replace("-", "_")


def _dist_info_name() -> str:
    version = _project()["project"]["version"]
    return f"{_normalized_name()}-{version}.dist-info"


def _write_dist_info(target: Path) -> None:
    project = _project()["project"]
    target.joinpath("METADATA").write_text(_metadata(project), encoding="utf-8")
    target.joinpath("WHEEL").write_text(_wheel(), encoding="utf-8")
    target.joinpath("entry_points.txt").write_text(_entry_points(project), encoding="utf-8")


def _metadata(project: dict) -> str:
    lines = [
        "Metadata-Version: 2.1",
        f"Name: {project['name']}",
        f"Version: {project['version']}",
        f"Summary: {project['description']}",
        f"Requires-Python: {project['requires-python']}",
    ]
    return "\n".join(lines) + "\n"


def _wheel() -> str:
    return "\n".join(
        [
            "Wheel-Version: 1.0",
            "Generator: harness-v2-backend 0.1.4",
            "Root-Is-Purelib: true",
            "Tag: py3-none-any",
        ]
    ) + "\n"


def _entry_points(project: dict) -> str:
    scripts = project.get("scripts", {})
    lines = ["[console_scripts]"]
    lines.extend(f"{name} = {target}" for name, target in sorted(scripts.items()))
    return "\n".join(lines) + "\n"
