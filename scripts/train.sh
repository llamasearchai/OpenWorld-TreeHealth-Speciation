#!/usr/bin/env bash
set -euo pipefail
OUT=${1:-artifacts/run_$(date +%s)}
openworld-tshm train --seed 42 --out-dir "$OUT"


