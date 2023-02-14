.PHONY: run-pre-commit run-isort run-black run-flake8

run-pre-commit:
	pre-commit run --all-files

run-isort:
	poetry run python -m isort .

run-black:
	poetry run python -m black . 

run-flake8:
	poetry run python -m flake8 . \
		--max-line-length 88 
