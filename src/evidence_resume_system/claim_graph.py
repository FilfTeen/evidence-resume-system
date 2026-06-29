from __future__ import annotations

from typing import Any

from .schema_validation import ValidationIssue


def unresolved_links(bundle: dict[str, Any]) -> list[ValidationIssue]:
    evidence_ids = {item.get("evidenceId") for item in bundle.get("evidenceItems", []) if isinstance(item, dict)}
    claim_ids = {item.get("claimId") for item in bundle.get("claims", []) if isinstance(item, dict)}
    issues: list[ValidationIssue] = []

    for claim in bundle.get("claims", []):
        if not isinstance(claim, dict):
            continue
        claim_id = claim.get("claimId", "unknown-claim")
        for evidence_id in claim.get("evidenceIds", []):
            if evidence_id not in evidence_ids:
                issues.append(ValidationIssue("missingEvidence", f"{claim_id} references missing evidence id {evidence_id}"))

    for decision in bundle.get("decisions", []):
        if not isinstance(decision, dict):
            continue
        decision_id = decision.get("decisionId", "unknown-decision")
        for claim_id in decision.get("relatedClaimIds", []):
            if claim_id not in claim_ids:
                issues.append(ValidationIssue("missingClaim", f"{decision_id} references missing claim id {claim_id}"))
        for evidence_id in decision.get("evidenceIds", []):
            if evidence_id not in evidence_ids:
                issues.append(ValidationIssue("missingEvidence", f"{decision_id} references missing evidence id {evidence_id}"))

    return issues
