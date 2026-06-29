# Demo Claim Bundle

This directory contains a synthetic claim bundle for exercising the validator and renderer. The data uses generic review items and ordinal labels. It is not based on a real-world subject or event sequence.

Run:

```bash
PYTHONPATH=src python3 -m evidence_resume_system validate examples/demo-claim-bundle
PYTHONPATH=src python3 -m evidence_resume_system render-report examples/demo-claim-bundle
```
