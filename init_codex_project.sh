#!/bin/bash

# === CONFIGURATION ===
PROJECT_NAME="mon_projet_codex"
BASE_DIR="./$PROJECT_NAME"

echo "🔧 Création du projet : $PROJECT_NAME"

# === STRUCTURE DE DOSSIERS ===
mkdir -p "$BASE_DIR"/{src,tests,docs}

# === FICHIERS PRINCIPAUX ===

# README.md
cat <<EOF > "$BASE_DIR/README.md"
# $PROJECT_NAME

Projet initialisé pour un environnement compatible Codex.

## Commandes utiles

- \`make run\` : lancer le script principal
- \`make lint\` : vérifier la syntaxe
- \`make test\` : lancer les tests
- \`make doc\` : générer la documentation
EOF

# pyproject.toml
cat <<EOF > "$BASE_DIR/pyproject.toml"
[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "Projet Python structuré pour intégration Codex"
requires-python = ">=3.10"
dependencies = []

[tool.poetry]
EOF

# Makefile
cat <<'EOF' > "$BASE_DIR/Makefile"
run:
	python3 src/main.py

lint:
	ruff lint src/ || flake8 src/

test:
	pytest tests/

doc:
	pdoc src --html --output-dir docs
EOF

# codex_instructions.txt
cat <<'EOF' > "$BASE_DIR/codex_instructions.txt"
# Codex Instructions : Respect des normes, robustesse, modularité
# Cf. https://chat.openai.com/docs/codex/configuration

- PEP8, docstrings, typage explicite
- pyproject.toml, Makefile, arborescence src/tests/docs
- Deux passes pour extraction documentaire
- Logs, gestion d'erreurs, tests unitaires
EOF

# src/main.py
cat <<'EOF' > "$BASE_DIR/src/main.py"
"""Script principal du projet Codex."""

def main() -> None:
    print("Projet Codex initialisé.")

if __name__ == "__main__":
    main()
EOF

# tests/test_main.py
cat <<'EOF' > "$BASE_DIR/tests/test_main.py"
def test_basic():
    assert True
EOF

echo "✅ Projet $PROJECT_NAME initialisé dans $BASE_DIR"
