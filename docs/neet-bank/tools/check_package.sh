#!/usr/bin/env bash
# Coordinator helper: validate one finished package against the sample and all merged batches, then write its
# key-free dump for the blind solver.   bash tools/check_package.sh <batch number> <package> <dump dir>
set -euo pipefail
cd "$(dirname "$0")/.."
k=$1; pkg=$2; out=$3
prefix=${pkg%%_*}; part=${pkg##*_}
file=$(printf "batches/parts/BATCH_%03d_%s_%s.json" "$k" "$prefix" "$part")
merged=$(ls batches/BATCH_0*.json 2>/dev/null | grep -v "BATCH_000" | sort | while read -r f; do
  n=$(basename "$f" .json); n=${n#BATCH_}; [ "$((10#$n))" -lt "$k" ] && echo "$f"; done || true)
python tools/qbank.py validate batches/BATCH_000_sample.json $merged "$file" \
  --plan "$(printf "batches/plans/BATCH_%03d_plan.json" "$k")" --package "$pkg" | grep -E "ERROR|WARN|error\(s\)"
mkdir -p "$out"
python tools/merge_batch.py dump "$k" "$pkg" > "$out/$pkg.txt"
echo "dump: $(grep -c '^NEET_' "$out/$pkg.txt") questions -> $out/$pkg.txt"
