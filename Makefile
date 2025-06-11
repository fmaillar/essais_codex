
# Makefile pour exécution du workflow de certification

YAML=workflow_certif.yaml
PHASE?=all

run:
	python main.py --yaml $(YAML)

phase:
	python main.py --yaml $(YAML) --phase $(PHASE)
