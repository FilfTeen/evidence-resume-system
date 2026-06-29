# Usage

The command line interface works with a claim bundle directory or with a direct path to `claim-bundle.json`.

```bash
PYTHONPATH=src python3 -m evidence_resume_system validate examples/demo-claim-bundle
PYTHONPATH=src python3 -m evidence_resume_system render-report examples/demo-claim-bundle
PYTHONPATH=src python3 -m evidence_resume_system privacy-scan .
```

The validator checks that:

- the bundle is marked synthetic when it is an example;
- evidence identifiers are unique;
- every claim links to at least one evidence item;
- every claim evidence link resolves;
- every decision references existing claims and evidence items;
- report settings contain a title and section list.

The renderer emits a deterministic Markdown review summary. The output is a validation summary, not a person-centered document.
