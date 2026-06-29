# Evidence Resume System

Evidence Resume System is a small Python package for checking neutral claim bundles. It validates JSON structure, checks that claims point to supporting evidence items, renders a deterministic review summary, and scans package text for obvious public-text privacy risks.

The included example is synthetic and uses generic review items. It does not describe a real-world subject or a submission artifact.

## What It Provides

- JSON schemas for evidence items, claims, decisions, and report settings.
- A command line interface for validation, privacy scanning, and deterministic Markdown summary output.
- A compact synthetic example for exercising the validation flow.
- Tests for schema checks, claim-to-evidence links, scanner behavior, and rendering.

## Install For Local Use

Use a Python 3.11 or newer environment, then run commands from the package root with `PYTHONPATH=src`:

```bash
PYTHONPATH=src python3 -m evidence_resume_system --help
PYTHONPATH=src python3 -m evidence_resume_system validate examples/demo-claim-bundle
PYTHONPATH=src python3 -m evidence_resume_system render-report examples/demo-claim-bundle
PYTHONPATH=src python3 -m evidence_resume_system privacy-scan .
```

## Data Shape

A claim bundle contains:

- `evidenceItems`: compact support records with stable identifiers and neutral summaries.
- `claims`: statements that list the evidence identifiers they depend on.
- `decisions`: review outcomes that explain whether a claim is approved, blocked, or needs review.
- `renderConfig`: settings for deterministic Markdown summary output.

Each synthetic bundle marks itself with `synthetic: true`.

## Boundaries

This package is for public package validation patterns and neutral demonstration data. It does not provide hiring, legal, compliance, or professional advice. Review any real use case with appropriate human judgment before relying on generated results.

Docs and examples use the CC-BY-4.0 license in `LICENSE`. Code, schemas, tests, and fixtures use the MIT license in `LICENSE-CODE`.
