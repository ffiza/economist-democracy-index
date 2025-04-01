.PHONY: all create-environment run-tests get-raw-data create-plots

all: create-environment run-tests get-raw-data create-plots

create-environment:
	python -m venv .venv
	.venv\Scripts\activate
	pip install -r requirements.txt

run-tests:
	python -m unittest discover tests

get-raw-data:
	python .\src\raw_data.py

create-plots:
	python .\src\static_plots.py
	python .\src\interactive_plots.py
