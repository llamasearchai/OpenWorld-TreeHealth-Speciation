# Changelog

## [Unreleased]

- Structured logging with JSON or rich formatting; global CLI logging options and `version` command.
- Dashboard: optional CORS, request ID middleware, and security headers.
- Plugins: file extension allowlists and size guards.
- OpenAI: Agents/Responses API integration with Chat Completions fallback; CLI `--use-agents` toggle; mocked tests.
- Docs & CI: fixed mkdocs config; docs CI workflow; GitHub Pages deployment workflow; make targets for docs.
- Tooling: pre-commit hooks (black, ruff, mypy) and Dependabot.
- Repo polish: logo in README, keywords in `pyproject.toml`, singular Author section (Nik Jois), cleaned placeholders.

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
