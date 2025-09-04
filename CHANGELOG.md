# Changelog

## [0.2.0] - 2025-09-03

- CHM percentile accuracy (exact 5th percentile per cell)
- Feature enrichment (p95/p50 height, crown area via convex hull fallback, density)
- Pydantic schemas for TreeRecord, Metrics; CLI validations and --dry-run for export
- LLM hardening with timeouts and safe auto fallback
- Provenance enriched with file hashes and env info; fsync on append
- Security checks for CSV size and field CSV schema
- Added docs (user, ops, dev), sample data, smoke and benchmark scripts
- CI workflow (lint, mypy, tests), coverage threshold to 95%
- Docker multi-stage, non-root runtime, healthcheck
- README cleanup (use `fallback` mode), version bump

