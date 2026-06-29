from pathlib import Path

from evidence_resume_system.privacy_scan import scan_path


def test_privacy_scan_detects_constructed_patterns(tmp_path: Path):
    sample = tmp_path / "sample.md"
    reserved_domain = "example" + ".invalid"
    email = "SYNTHETIC_EMAIL_TRIGGER" + "@" + reserved_domain
    link = "https:" + "//" + reserved_domain + "/check"
    path = "/" + "Users" + "/" + "sample" + "/" + "demo.txt"
    marker = "tok" + "en=" + "SYNTHETIC_" + "TOKEN_" + "TRIGGER_DO_NOT_USE_" + "0000"
    heading = "# " + "Experience"
    sample.write_text("\n".join([email, link, path, marker, heading]), encoding="utf-8")

    kinds = {finding.kind for finding in scan_path(sample)}
    assert {"email", "url", "local-path", "token-assignment", "resume-heading"}.issubset(kinds)


def test_privacy_scan_passes_neutral_fixture():
    findings = scan_path(Path("examples/demo-claim-bundle"))
    assert findings == []
