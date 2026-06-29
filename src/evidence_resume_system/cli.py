from __future__ import annotations

import argparse
from pathlib import Path
import sys

from . import __version__
from .load import BundleLoadError, display_path, load_json
from .privacy_scan import scan_path
from .render_markdown import render_report
from .schema_validation import validate_bundle


def cmd_validate(args: argparse.Namespace) -> int:
    try:
        bundle = load_json(Path(args.path))
    except BundleLoadError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    issues = validate_bundle(bundle)
    if issues:
        for issue in issues:
            print(str(issue), file=sys.stderr)
        return 1
    print(f"PASS validation {display_path(Path(args.path))}")
    return 0


def cmd_render_report(args: argparse.Namespace) -> int:
    try:
        bundle = load_json(Path(args.path))
    except BundleLoadError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    issues = validate_bundle(bundle)
    if issues:
        for issue in issues:
            print(str(issue), file=sys.stderr)
        return 1
    output = render_report(bundle)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


def cmd_privacy_scan(args: argparse.Namespace) -> int:
    findings = scan_path(Path(args.path))
    if findings:
        for finding in findings:
            print(f"{finding.path}:{finding.line}: {finding.kind}: {finding.excerpt}")
        return 1
    print(f"PASS privacy scan {display_path(Path(args.path))}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="evidence-resume-system")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate a synthetic claim bundle")
    validate.add_argument("path")
    validate.set_defaults(func=cmd_validate)

    render = subparsers.add_parser("render-report", help="render a deterministic Markdown review summary")
    render.add_argument("path")
    render.add_argument("--output")
    render.set_defaults(func=cmd_render_report)

    privacy = subparsers.add_parser("privacy-scan", help="scan text files for generic public-text privacy patterns")
    privacy.add_argument("path")
    privacy.set_defaults(func=cmd_privacy_scan)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
