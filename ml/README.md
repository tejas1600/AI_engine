# ML layer: incident classifier with MLflow

What this is: a model that reads a window of log lines and says what kind of incident it is (memory leak, database down, bad deploy, expired certificate, locked account, full disk, or normal). It is tracked, versioned and served through the MLflow model registry. Later, the AI incident agent calls this model as one of its tools.

## Files

| File | Purpose |
|------|---------|
| `simulator.py` | Generates log windows with a known incident type (the answer key) |
| `train.py` | Trains a model variant, logs params, metrics and a confusion matrix to MLflow, registers a new version |
| `registry.py` | Status, promote, rollback, quality gate, and load-by-alias prediction |
| `run_all.sh` | Rebuilds everything from scratch and runs the full flow |
| `requirements.txt` | Python dependencies |

## Concepts (read these first, 10 minutes)

- **Experiment and run:** an experiment groups attempts. A run is one attempt. You log params (inputs), metrics (scores) and artifacts (files).
- **Model registry:** a versioned catalogue. Every registration creates the next version (v1, v2, v3).
- **Alias:** a movable label pointing at one version. Serving code loads `models:/incident-classifier@production` and never hardcodes a version.
- **Rollback:** moving the alias back to the previous version. No rebuild, no redeploy.
- **Quality gate:** a rule that blocks promotion unless the candidate beats a threshold. The gate exits with code 1 on failure, so Jenkins can fail a pipeline on it later.
- **Confusion matrix:** shows which classes get mixed up, which accuracy alone hides.

## Run it

```
pip install -r requirements.txt
bash run_all.sh
```

Browse the tracking UI (optional):

```
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

## What I measured (rerun to confirm)

| Version | Variant | Features | Accuracy | Macro F1 |
|---------|---------|----------|----------|----------|
| v1 | baseline | 15 word counts, Naive Bayes | 0.570 | 0.571 |
| v2 | improved | TF-IDF unigrams and bigrams, Logistic Regression | 0.996 | 0.996 |

Rollback test: with `production` pointed at v1, a 7-sample check got 2 of 7 right. After moving the alias back to v2, it got 7 of 7. No code or service changed between those two checks.

## Honest limits

- The data is synthetic. The simulator uses templated log lines, so the 0.996 score is much higher than real logs would give. Treat it as a pipeline test, not as proof the model works on production logs.
- The next step that makes this real: feed it logs from the chaos engine on the platform, and later a public dataset such as Loghub, then compare scores.
- The model only classifies. The AI agent adds the investigation, evidence and explanation.

## Break-it exercises (do these, then write 5 lines each in docs/)

1. **Poisoned data:** in `simulator.py`, make `normal` windows include `ERROR connection refused host=db-primary`. Retrain. Which class gets confused with `normal`? Check the confusion matrix in the UI.
2. **Gate in action:** train a third version with `--per-class 10`. Run `python registry.py gate 3`. Why does a tiny dataset fail the gate?
3. **Drift:** change the log wording in `SYMPTOMS` (for example "connection refused" becomes "conn rejected") and score v2 on the new text without retraining. What happens, and what would you monitor in production to notice it?
4. **Rollback drill:** promote a bad version on purpose, run `python registry.py predict`, then roll back. Time how long recovery takes.

## Interview talking points

- Why serve by alias and not by version number
- What a quality gate protects against, and why it should live in CI
- Why accuracy alone is not enough (confusion matrix, per-class errors)
- Why synthetic data results must be labelled as such
- How this model becomes a tool the incident agent calls
