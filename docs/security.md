# Security Notes

- Inputs:
  - CSV size limited by `OW_TSHM_MAX_CSV_MB` (default 50 MB).
  - Field CSV validation requires `species` and one of `height` or `age`.
- CLI:
  - Validates numeric ranges and file existence for demo flows.
- LLM:
  - Optional, disabled by default; 3s timeout on local LLM; deterministic fallback.
- Web:
  - Demo dashboard exposes only static pages and read-only endpoints.
- Dependencies:
  - `pip-audit` included in CI workflow; failures reported.

