.PHONY: start-cli start-web 

start-cli:
	python main.py 

start-web:
	python web/app.py

run-local-precommit-check:
	pre-commit run --all-files
