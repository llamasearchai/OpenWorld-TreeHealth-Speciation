#!/usr/bin/env bash
set -euo pipefail

openworld-tshm process-demo --eps 1.5 --min-samples 5 >/dev/null
openworld-tshm train --seed 42 --out-dir artifacts/run_42 >/dev/null
openworld-tshm export-sqlite --db forest.db >/dev/null
openworld-tshm report --out reports/latest.html --use-llm fallback >/dev/null
echo OK

