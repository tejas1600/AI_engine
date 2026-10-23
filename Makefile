.PHONY: help ml-run ml-ui hooks

help:
	@echo "make ml-run   run the full ML flow (train, gate, promote, rollback)"
	@echo "make ml-ui    open the MLflow tracking UI on port 5000"
	@echo "make hooks    install pre-commit hooks (secret scanning)"

ml-run:
	cd ml && bash run_all.sh

ml-ui:
	cd ml && mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000

hooks:
	pip install pre-commit && pre-commit install
