#!/usr/bin/env bash
set -euo pipefail
DB=${1:-forest.db}
openworld-tshm export-sqlite --db "$DB"
datasette serve "$DB" -m datasette.yml


