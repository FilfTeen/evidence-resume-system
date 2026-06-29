from evidence_resume_system.cli import main


def test_validate_command_passes(capsys):
    assert main(["validate", "examples/demo-claim-bundle"]) == 0
    captured = capsys.readouterr()
    assert "PASS validation examples/demo-claim-bundle" in captured.out


def test_render_command_prints_report(capsys):
    assert main(["render-report", "examples/demo-claim-bundle"]) == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("# Demo Quality Review Report")


def test_privacy_scan_command_passes(capsys):
    assert main(["privacy-scan", "examples/demo-claim-bundle"]) == 0
    captured = capsys.readouterr()
    assert "PASS privacy scan examples/demo-claim-bundle" in captured.out
