from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class BundleLoadError(ValueError):
    pass


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.name


def bundle_file(path: Path) -> Path:
    if path.is_dir():
        return path / "claim-bundle.json"
    return path


def load_json(path: Path) -> Any:
    target = bundle_file(path)
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BundleLoadError(f"missing JSON file: {display_path(target)}") from exc
    except json.JSONDecodeError as exc:
        raise BundleLoadError(f"invalid JSON in {display_path(target)}: line {exc.lineno}") from exc
