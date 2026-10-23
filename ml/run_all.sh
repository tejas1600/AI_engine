#!/usr/bin/env bash
# Rebuilds the ML layer from scratch and runs the full flow:
# train v1 and v2, gate, promote, predict, rollback, restore.
set -euo pipefail
cd "$(dirname "$0")"
export MLFLOW_DISABLE_AGENT_HINT=1

rm -f mlflow.db
rm -rf mlruns mlartifacts

echo "== 1. train baseline (v1) and improved (v2) =="
python3 train.py --variant baseline 2>&1 | grep "^variant="
python3 train.py --variant improved 2>&1 | grep "^variant="

echo
echo "== 2. quality gate: v1 should fail, v2 should pass =="
if python3 registry.py gate 1 2>&1 | grep GATE; then :; fi
python3 registry.py gate 2 2>&1 | grep -E "GATE|alias"

echo
echo "== 3. serve from @production =="
python3 registry.py predict 2>&1 | grep -v INFO

echo
echo "== 4. rollback to v1 (no redeploy) =="
python3 registry.py promote 1 2>&1 | grep alias
python3 registry.py predict 2>&1 | grep -E "serving|correct"

echo
echo "== 5. restore v2 =="
python3 registry.py promote 2 2>&1 | grep alias
python3 registry.py status 2>&1 | grep -v INFO
