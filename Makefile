PYTHON ?= python3
VENV ?= .venv

.PHONY: venv install run test compile clean

venv:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip

install: venv
	$(VENV)/bin/pip install -e .[dev]

run:
	$(VENV)/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	$(VENV)/bin/python -m pytest -q

compile:
	$(VENV)/bin/python -m compileall app tests

clean:
	rm -rf $(VENV) .pytest_cache
