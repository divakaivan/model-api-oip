.PHONY: help start test lint

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  start     Start the API"
	@echo "  test      Run tests with pytest"
	@echo "  lint      Run pre-commit hooks"

.DEFAULT_GOAL := help

start:
	python -m src.main

test:
	python -m pytest

lint:
	pre-commit run --all-files
