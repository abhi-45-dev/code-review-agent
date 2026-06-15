# Prompt Versions

## code_review_prompt_v1

Status: Stable

Changes:
- Added evidence-based findings
- Reduced false positives
- Allowed empty findings
- Prevented speculative vulnerabilities
- Improvement suggestions require specific code evidence
- Prompt moved outside application code

Validation:
- sample2.c -> 0 findings
- nested_repo/main.py -> SQL injection detected
- Integration tests passing

Notes:
This is the current production prompt and should be used as the baseline for future prompt experiments.
