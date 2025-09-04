# Operator Guide

- Environment variables:
  - `OW_TSHM_DATA_DIR`: data directory (default `./data`)
  - `OW_TSHM_ARTIFACTS_DIR`: artifacts directory (default `./artifacts`)
  - `OW_TSHM_PROVENANCE_LEDGER`: provenance ledger path (default `./provenance/ledger.jsonl`)
  - `OPENAI_API_KEY`, `OPENAI_MODEL`: enable OpenAI LLM mode
  - `OLLAMA_MODEL`: enable local LLM via `llm` CLI
  - `OW_TSHM_MAX_CSV_MB`: size guard for CSV ingestion (default `50`)

- Smoke test: `./scripts/smoke.sh` prints `OK` on success.
- Benchmarks: `./scripts/benchmark.sh` prints step timings.

