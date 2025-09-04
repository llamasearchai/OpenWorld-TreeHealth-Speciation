# User Guide

- Install: `pip install -e ".[dev]"`
- Demo: `openworld-tshm process-demo`
- Train: `openworld-tshm train --seed 42 --out-dir artifacts/run_42`
- Export: `openworld-tshm export-sqlite --db forest.db`
- Report: `openworld-tshm report --out reports/latest.html --use-llm fallback`
- Dashboard: `openworld-tshm dashboard --host 0.0.0.0 --port 8000`

Use `--help` on each command for flags and examples.

