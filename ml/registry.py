"""Model registry operations: promote, roll back, and serve by alias.

Concept: serving code never says "use version 2". It says "use whatever the
production alias points at" (models:/incident-classifier@production).
Promotion and rollback are then just moving the alias. No redeploy needed.

Usage:
    python registry.py status
    python registry.py promote 1          # point production at version 1
    python registry.py promote 2          # point production at version 2
    python registry.py predict            # load @production and classify a sample
    python registry.py gate 2             # promote only if the quality gate passes
"""
import os
import sys

import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow import MlflowClient

from simulator import make_window
import random

HERE = os.path.dirname(os.path.abspath(__file__))
mlflow.set_tracking_uri(f"sqlite:///{HERE}/mlflow.db")
MODEL_NAME = "incident-classifier"
ALIAS = "production"
MIN_ACCURACY = 0.90  # quality gate: a candidate must beat this on the test set

client = MlflowClient()


def status():
    versions = client.search_model_versions(f"name='{MODEL_NAME}'")
    try:
        prod = client.get_model_version_by_alias(MODEL_NAME, ALIAS).version
    except Exception:
        prod = None
    print(f"production alias -> version {prod}")
    for v in sorted(versions, key=lambda x: int(x.version)):
        run = client.get_run(v.run_id)
        m = run.data.metrics
        tag = "  <-- production" if v.version == prod else ""
        print(f"  v{v.version}: variant={run.data.params.get('variant')} "
              f"accuracy={m.get('accuracy'):.3f} macro_f1={m.get('macro_f1'):.3f}{tag}")


def promote(version: str):
    client.set_registered_model_alias(MODEL_NAME, ALIAS, version)
    print(f"production alias now points at version {version}")


def gate(version: str):
    v = client.get_model_version(MODEL_NAME, version)
    acc = client.get_run(v.run_id).data.metrics["accuracy"]
    if acc >= MIN_ACCURACY:
        print(f"GATE PASSED: v{version} accuracy {acc:.3f} >= {MIN_ACCURACY}")
        promote(version)
    else:
        print(f"GATE FAILED: v{version} accuracy {acc:.3f} < {MIN_ACCURACY}. Not promoted.")
        sys.exit(1)


def predict():
    model = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}@{ALIAS}")
    version = client.get_model_version_by_alias(MODEL_NAME, ALIAS).version
    rng = random.Random(123)
    samples = ["memory_leak", "db_down", "cert_expired", "account_locked", "bad_deploy", "disk_full", "normal"]
    df = pd.DataFrame({"logs": [make_window(s, rng) for s in samples]})
    preds = model.predict(df)
    right = 0
    print(f"serving version {version} via @{ALIAS}")
    for truth, p in zip(samples, preds):
        ok = truth == p
        right += ok
        print(f"  truth={truth:15s} predicted={p:15s} {'OK' if ok else 'WRONG'}")
    print(f"{right}/{len(samples)} correct on this sample")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "status":
        status()
    elif cmd == "promote":
        promote(sys.argv[2])
    elif cmd == "gate":
        gate(sys.argv[2])
    elif cmd == "predict":
        predict()
    else:
        print(__doc__)
