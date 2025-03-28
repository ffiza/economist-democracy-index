.PHONY: create-environment

create-environment:
	python -m venv .venv
	.venv\Scripts\activate && pip install -r requirements.txt

create-plots:
	python .\src\plots.py

run-tests:
	python -m unittest discover tests
