"""Correspond à l'étape `step2_check_preuves` définie dans `workflow_certif.yaml`.

Description YAML :
  - id: step2_check_preuves
  - description: Vérifie la présence de preuves de conception et de test pour chaque exigence applicable.
  - input: data/exigences.xlsx
  - output: audit/preuves_manquantes.csv

Instructions Codex :
→ Implémenter cette logique dans ce fichier.
→ Utiliser du code clair, modulaire, robuste (pandas, pathlib, logging, etc.).
→ Voir aussi `README.md` et `AGENTS.md` pour le contexte global.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

LOG_FILE = Path("logs/check_preuves.log")
AUDIT_FILE = Path("audit/preuves_manquantes.csv")
DATA_FILE = Path("data/preuves.xlsx")


def setup_logger() -> None:
    """Configure logging."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def check_preuves(filepath: Path) -> pd.DataFrame:
    """Return rows missing design or test evidence."""
    df = pd.read_excel(filepath, engine="openpyxl")
    mask = (
        (df.get("Applicability") == "Oui")
        & (df.get("Preuve_conception").isna() | df.get("Preuve_test").isna())
    )
    return df.loc[mask]


def main() -> None:
    """Entry point."""
    setup_logger()

    if not DATA_FILE.exists():
        logging.error("Fichier %s introuvable", DATA_FILE)
        sys.exit(1)

    try:
        invalid_rows = check_preuves(DATA_FILE)
    except Exception as exc:
        logging.exception("Erreur lors de la lecture du fichier: %s", exc)
        sys.exit(1)

    if not invalid_rows.empty:
        AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
        invalid_rows.to_csv(AUDIT_FILE, index=False)
        logging.warning("Preuves manquantes: %d", len(invalid_rows))
        sys.exit(1)

    logging.info("Toutes les preuves sont presentes")
    sys.exit(0)


if __name__ == "__main__":
    main()
