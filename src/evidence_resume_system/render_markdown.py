from __future__ import annotations

from typing import Any


def render_report(bundle: dict[str, Any]) -> str:
    config = bundle["renderConfig"]
    lines: list[str] = [f"# {config['title']}", "", f"Bundle: `{bundle['bundleId']}`", ""]

    sections = config.get("includeSections", [])
    if "claims" in sections:
        lines.extend(["## Claim Review", ""])
        for claim in bundle.get("claims", []):
            evidence = ", ".join(f"`{item}`" for item in claim.get("evidenceIds", []))
            lines.append(f"- `{claim['claimId']}` {claim['claimStatus']}: {claim['statement']} Evidence: {evidence}.")
        lines.append("")

    if "decisions" in sections:
        lines.extend(["## Decisions", ""])
        for decision in bundle.get("decisions", []):
            claims = ", ".join(f"`{item}`" for item in decision.get("relatedClaimIds", []))
            lines.append(f"- `{decision['decisionId']}` {decision['decisionStatus']}: {decision['rationale']} Claims: {claims}.")
        lines.append("")

    if "evidenceSummary" in sections:
        lines.extend(["## Evidence Summary", ""])
        for item in bundle.get("evidenceItems", []):
            lines.append(f"- `{item['evidenceId']}` {item['kind']}: {item['summary']}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
