from __future__ import annotations

from collections.abc import Mapping
from typing import Any

ALLOWED_EVIDENCE_KINDS = {"check", "note", "review"}
ALLOWED_STATUSES = {"approved", "blocked", "reviewRequired"}
ALLOWED_SECTIONS = {"claims", "decisions", "evidenceSummary"}


class ValidationIssue:
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


def _require_mapping(value: Any, label: str, issues: list[ValidationIssue]) -> bool:
    if not isinstance(value, Mapping):
        issues.append(ValidationIssue("type", f"{label} must be an object"))
        return False
    return True


def _require_string(item: Mapping[str, Any], key: str, label: str, issues: list[ValidationIssue]) -> None:
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        issues.append(ValidationIssue("field", f"{label}.{key} must be a non-empty string"))


def _require_list(item: Mapping[str, Any], key: str, label: str, issues: list[ValidationIssue]) -> None:
    value = item.get(key)
    if not isinstance(value, list):
        issues.append(ValidationIssue("field", f"{label}.{key} must be a list"))


def validate_bundle(bundle: Any) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not _require_mapping(bundle, "bundle", issues):
        return issues

    if bundle.get("schemaVersion") != "claim-bundle-1":
        issues.append(ValidationIssue("schemaVersion", "bundle.schemaVersion must be claim-bundle-1"))
    if bundle.get("synthetic") is not True:
        issues.append(ValidationIssue("synthetic", "example bundles must set synthetic to true"))
    _require_string(bundle, "bundleId", "bundle", issues)

    evidence_items = bundle.get("evidenceItems")
    claims = bundle.get("claims")
    decisions = bundle.get("decisions")
    render_config = bundle.get("renderConfig")

    if not isinstance(evidence_items, list):
        issues.append(ValidationIssue("evidenceItems", "bundle.evidenceItems must be a list"))
        evidence_items = []
    if not isinstance(claims, list):
        issues.append(ValidationIssue("claims", "bundle.claims must be a list"))
        claims = []
    if not isinstance(decisions, list):
        issues.append(ValidationIssue("decisions", "bundle.decisions must be a list"))
        decisions = []

    evidence_ids: set[str] = set()
    for index, item in enumerate(evidence_items):
        label = f"evidenceItems[{index}]"
        if not _require_mapping(item, label, issues):
            continue
        _require_string(item, "evidenceId", label, issues)
        _require_string(item, "summary", label, issues)
        if item.get("kind") not in ALLOWED_EVIDENCE_KINDS:
            issues.append(ValidationIssue("kind", f"{label}.kind has an unsupported value"))
        evidence_id = item.get("evidenceId")
        if isinstance(evidence_id, str):
            if evidence_id in evidence_ids:
                issues.append(ValidationIssue("duplicate", f"duplicate evidence id {evidence_id}"))
            evidence_ids.add(evidence_id)
        if "supports" in item and not isinstance(item.get("supports"), list):
            issues.append(ValidationIssue("supports", f"{label}.supports must be a list when present"))

    claim_ids: set[str] = set()
    for index, item in enumerate(claims):
        label = f"claims[{index}]"
        if not _require_mapping(item, label, issues):
            continue
        _require_string(item, "claimId", label, issues)
        _require_string(item, "statement", label, issues)
        if item.get("claimStatus") not in ALLOWED_STATUSES:
            issues.append(ValidationIssue("claimStatus", f"{label}.claimStatus has an unsupported value"))
        _require_list(item, "evidenceIds", label, issues)
        claim_id = item.get("claimId")
        if isinstance(claim_id, str):
            if claim_id in claim_ids:
                issues.append(ValidationIssue("duplicate", f"duplicate claim id {claim_id}"))
            claim_ids.add(claim_id)
        for evidence_id in item.get("evidenceIds", []):
            if evidence_id not in evidence_ids:
                issues.append(ValidationIssue("missingEvidence", f"{label} references missing evidence id {evidence_id}"))

    for index, item in enumerate(decisions):
        label = f"decisions[{index}]"
        if not _require_mapping(item, label, issues):
            continue
        _require_string(item, "decisionId", label, issues)
        _require_string(item, "rationale", label, issues)
        if item.get("decisionStatus") not in ALLOWED_STATUSES:
            issues.append(ValidationIssue("decisionStatus", f"{label}.decisionStatus has an unsupported value"))
        _require_list(item, "relatedClaimIds", label, issues)
        for claim_id in item.get("relatedClaimIds", []):
            if claim_id not in claim_ids:
                issues.append(ValidationIssue("missingClaim", f"{label} references missing claim id {claim_id}"))
        for evidence_id in item.get("evidenceIds", []):
            if evidence_id not in evidence_ids:
                issues.append(ValidationIssue("missingEvidence", f"{label} references missing evidence id {evidence_id}"))

    if _require_mapping(render_config, "renderConfig", issues):
        _require_string(render_config, "title", "renderConfig", issues)
        sections = render_config.get("includeSections")
        if not isinstance(sections, list) or not sections:
            issues.append(ValidationIssue("includeSections", "renderConfig.includeSections must be a non-empty list"))
        else:
            for section in sections:
                if section not in ALLOWED_SECTIONS:
                    issues.append(ValidationIssue("includeSections", f"unsupported report section {section}"))

    return issues


def assert_valid_bundle(bundle: Any) -> None:
    issues = validate_bundle(bundle)
    if issues:
        joined = "\n".join(str(issue) for issue in issues)
        raise ValueError(joined)
