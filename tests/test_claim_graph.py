import json
from pathlib import Path

from evidence_resume_system.claim_graph import unresolved_links


def test_claim_graph_reports_missing_evidence():
    bundle = json.loads(Path("tests/fixtures/invalid_missing_evidence.json").read_text(encoding="utf-8"))
    issues = unresolved_links(bundle)
    assert [issue.code for issue in issues] == ["missingEvidence"]
