PYTHON=python3
YAML=workflow_certif.yaml

run:
	$(PYTHON) main.py --yaml $(YAML)

lint:
	ruff scripts main.py || flake8 scripts main.py

test:
	pytest tests

doc:
	pdoc --html --output-dir docs scripts
