.PHONY: all prepare_dirs check_exigences check_mop check_preuves \
        soumettre_dossier gerer_retours analyse_impact_retours synthese_retours \
        run lint test doc

all: prepare_dirs check_exigences check_mop check_preuves soumettre_dossier gerer_retours analyse_impact_retours synthese_retours

prepare_dirs:
	mkdir -p logs audit

check_exigences:
	@echo "=== Vérification des exigences ==="
	python scripts/check_exigences.py >> logs/check_exigences.log 2>&1 || exit 1

check_mop:
	@echo "=== Vérification des MOP ==="
	python scripts/check_mop.py >> logs/check_mop.log 2>&1 || exit 1

check_preuves:
	@echo "=== Vérification des preuves ==="
	python scripts/check_preuves.py >> logs/check_preuves.log 2>&1 || exit 1

soumettre_dossier:
	@echo "=== Soumission du dossier ==="
	python scripts/soumettre_dossier.py >> logs/soumettre_dossier.log 2>&1 || exit 1

gerer_retours:
	@echo "=== Gestion des retours des évaluateurs ==="
	python scripts/gerer_retours.py >> logs/gerer_retours.log 2>&1 || exit 1

analyse_impact_retours:
	@echo "=== Analyse de l'impact des retours ==="
	python scripts/analyse_retours.py >> logs/analyse_retours.log 2>&1 || exit 1

synthese_retours:
	@echo "=== Synthèse des retours par exigence ==="
	python scripts/synthese_retours.py >> logs/synthese_retours.log 2>&1 || exit 1

run:
	python main.py

lint:
	ruff check .

test:
	pytest -q

doc:
	pdoc --html --output-dir docs main.py scripts
