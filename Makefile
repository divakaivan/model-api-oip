start:
	python -m src.main

test:
	python -m pytest

lint:
	pre-commit run --all-files
