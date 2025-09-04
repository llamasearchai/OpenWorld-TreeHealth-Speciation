#!/usr/bin/env bash
set -euo pipefail
start=$(date +%s)
openworld-tshm process-demo --eps 1.8 --min-samples 5 >/dev/null
mid1=$(date +%s)
openworld-tshm train --seed 42 --out-dir artifacts/bench >/dev/null
mid2=$(date +%s)
openworld-tshm report --out reports/bench.html --use-llm fallback >/dev/null
end=$(date +%s)
echo "process-demo: $((mid1-start))s, train: $((mid2-mid1))s, report: $((end-mid2))s"

