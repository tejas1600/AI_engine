"""Train an incident classifier and track it with MLflow.

Concepts in this file:
- Experiment: a named group of runs you want to compare.
- Run: one training attempt. We log params (inputs), metrics (scores) and
  artifacts (files such as a confusion matrix).
- Model registry: a versioned catalogue. Each registered model gets v1, v2...
  Aliases (like "production") point at one version and can be moved later.

Usage:
    python train.py --variant baseline
    python train.py --variant improved
"""
import argparse
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.models import infer_signature
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from simulator import LABELS, make_dataset

HERE = os.path.dirname(os.path.abspath(__file__))
TRACKING_URI = f"sqlite:///{HERE}/mlflow.db"
EXPERIMENT = "incident-classifier"
MODEL_NAME = "incident-classifier"

# Only alphabetic tokens: numbers such as ids and latencies are noise, and
# ignoring them is a cheap way to normalise logs.
TOKEN_PATTERN = r"[A-Za-z_]{3,}"


def build_pipeline(variant: str):
    if variant == "baseline":
        # Deliberately simple: 15 word counts and Naive Bayes.
        vec = CountVectorizer(token_pattern=TOKEN_PATTERN, max_features=15)
        clf = MultinomialNB()
        params = {"vectorizer": "CountVectorizer", "max_features": 15,
                  "ngram_range": "1-1", "classifier": "MultinomialNB"}
    elif variant == "improved":
        vec = TfidfVectorizer(token_pattern=TOKEN_PATTERN, ngram_range=(1, 2),
                              min_df=2, sublinear_tf=True)
        clf = LogisticRegression(max_iter=1000, C=5.0)
        params = {"vectorizer": "TfidfVectorizer", "max_features": "all",
                  "ngram_range": "1-2", "classifier": "LogisticRegression", "C": 5.0}
    else:
        raise ValueError(f"unknown variant {variant}")
    pipe = Pipeline([
        ("features", ColumnTransformer([("text", vec, "logs")])),
        ("clf", clf),
    ])
    return pipe, params


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=["baseline", "improved"], required=True)
    ap.add_argument("--per-class", type=int, default=150)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT)

    df = make_dataset(per_class=args.per_class, seed=args.seed)
    X_train, X_test, y_train, y_test = train_test_split(
        df[["logs"]], df["label"], test_size=0.25, random_state=42, stratify=df["label"]
    )

    pipe, params = build_pipeline(args.variant)

    with mlflow.start_run(run_name=args.variant) as run:
        mlflow.log_params({**params, "variant": args.variant,
                           "per_class": args.per_class, "seed": args.seed,
                           "train_rows": len(X_train), "test_rows": len(X_test)})
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)

        acc = accuracy_score(y_test, pred)
        f1 = f1_score(y_test, pred, average="macro")
        mlflow.log_metrics({"accuracy": acc, "macro_f1": f1})

        # Artifact: confusion matrix picture (black and white).
        fig, ax = plt.subplots(figsize=(7, 6))
        ConfusionMatrixDisplay.from_predictions(
            y_test, pred, labels=LABELS, xticks_rotation=45, cmap="Greys", ax=ax
        )
        ax.set_title(f"Confusion matrix: {args.variant}")
        fig.tight_layout()
        cm_path = os.path.join(HERE, f"confusion_{args.variant}.png")
        fig.savefig(cm_path, dpi=120)
        plt.close(fig)
        mlflow.log_artifact(cm_path)

        # Log the model AND register it. Each call creates a new version.
        signature = infer_signature(X_test, pred)
        mlflow.sklearn.log_model(
            pipe,
            name="model",
            signature=signature,
            input_example=X_test.head(2),
            registered_model_name=MODEL_NAME,
        )
        print(f"variant={args.variant} accuracy={acc:.3f} macro_f1={f1:.3f} run_id={run.info.run_id}")


if __name__ == "__main__":
    main()
