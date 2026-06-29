import json
from pathlib import Path

from evidence_resume_system.schema_validation import validate_bundle


def test_valid_bundle_fixture_passes():
    bundle = json.loads(Path("tests/fixtures/valid_bundle.json").read_text(encoding="utf-8"))
    assert validate_bundle(bundle) == []


def test_missing_evidence_is_reported():
    bundle = json.loads(Path("tests/fixtures/invalid_missing_evidence.json").read_text(encoding="utf-8"))
    issues = validate_bundle(bundle)
    assert any(issue.code == "missingEvidence" for issue in issues)
