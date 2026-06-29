from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

_TEXT_SUFFIXES = {".md", ".py", ".json", ".toml", ".txt", ""}
_HOME_MARKERS = ["/" + "Users" + "/", "/" + "home" + "/"]


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    kind: str
    excerpt: str


EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d{1,3}[ .-]?)?(?:\(?\d{3}\)?[ .-]?\d{3}[ .-]?\d{4})(?!\w)")
URL_RE = re.compile(r"\bhttps?://[^\s)\]]+", re.IGNORECASE)
TOKEN_ASSIGNMENT_RE = re.compile(r"(?i)\b(?:api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}")
METADATA_FIELD_RE = re.compile(r"(?im)^\s*(authors|maintainers|homepage|repository|funding|bug[_-]?tracker|project\.urls)\s*=")
RESUME_HEADING_RE = re.compile(r"(?im)^#{1,3}\s+(education|experience|work history|employment|skills|objective|profile|curriculum vitae)\s*$")


def _safe_excerpt(line: str) -> str:
    return line.strip()[:96]


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.name


def iter_text_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    ignored_dirs = {".git", "__pycache__", ".pytest_cache", ".venv", "build", "dist"}
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if any(part in ignored_dirs for part in path.parts):
            continue
        if path.is_file() and path.suffix in _TEXT_SUFFIXES:
            files.append(path)
    return files


def scan_text(text: str, display_path: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        checks = [
            ("email", EMAIL_RE.search(line)),
            ("phone", PHONE_RE.search(line)),
            ("url", URL_RE.search(line)),
            ("token-assignment", TOKEN_ASSIGNMENT_RE.search(line)),
            ("metadata-route", METADATA_FIELD_RE.search(line)),
            ("resume-heading", RESUME_HEADING_RE.search(line)),
        ]
        if any(marker in line for marker in _HOME_MARKERS):
            findings.append(Finding(display_path, line_number, "local-path", _safe_excerpt(line)))
        for kind, match in checks:
            if match:
                findings.append(Finding(display_path, line_number, kind, _safe_excerpt(line)))
    return findings


def scan_path(path: Path) -> list[Finding]:
    root = path if path.is_dir() else path.parent
    findings: list[Finding] = []
    for file_path in iter_text_files(path):
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        findings.extend(scan_text(text, _relative(file_path, root)))
    return findings
