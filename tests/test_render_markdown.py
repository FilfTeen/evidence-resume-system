from pathlib import Path

from evidence_resume_system.load import load_json
from evidence_resume_system.render_markdown import render_report


def test_rendered_demo_report_matches_expected():
    bundle = load_json(Path("examples/demo-claim-bundle"))
    expected = Path("examples/demo-claim-bundle/expected-report.md").read_text(encoding="utf-8")
    assert render_report(bundle) == expected
