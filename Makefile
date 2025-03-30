.PHONY: all create-environment run-tests create-plots

all: create-environment run-tests create-plots

create-environment:
	python -m venv .venv
	.venv\Scripts\activate
	pip install -r requirements.txt

run-tests:
	python -m unittest discover tests

create-plots:
	python .\src\plots.py
