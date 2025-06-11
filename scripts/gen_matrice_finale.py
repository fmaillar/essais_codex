"""
Correspond à l'étape `step3_generate_matrix` définie dans `workflow_certif.yaml`.

Description YAML :
  - id: step3_generate_matrix
  - description: Génère une matrice consolidée avec l’ensemble des exigences, justifications et preuves.
  - input: data/exigences.xlsx
  - output: out/matrice_certif.xlsx

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

LOG_FILE = Path("logs/gen_matrice_finale.log")
OUTPUT_FILE = Path("audit/matrice_finale.xlsx")
EVIDENCE_FILE = Path("data/preuves.xlsx")


def setup_logger() -> None:
    """Configure logging to file."""
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def generate_matrix(filepath: Path) -> pd.DataFrame:
    """Return compliant evidence rows from the Excel file.

    Parameters
    ----------
    filepath : Path
        Path to the evidence Excel file.

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame containing only valid entries.
    """
    df = pd.read_excel(filepath, engine="openpyxl")

    applicability_col = df.filter(regex="(?i)applicab").columns[0]
    design_col = df.filter(regex="(?i)preuve.*conception").columns[0]
    test_col = df.filter(regex="(?i)preuve.*test").columns[0]

    mask = (
        df[applicability_col].str.lower() == "oui"
    ) & df[design_col].notna() & df[test_col].notna()

    return df.loc[mask]


def main() -> None:
    """Generate the final matrix and export it to ``OUTPUT_FILE``."""
    setup_logger()

    if not EVIDENCE_FILE.exists():
        logging.error("Fichier %s introuvable", EVIDENCE_FILE)
        sys.exit(1)

    try:
        matrix = generate_matrix(EVIDENCE_FILE)
    except Exception as exc:  # fallback for unexpected format
        logging.exception("Erreur lors du traitement du fichier: %s", exc)
        sys.exit(1)

    try:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        matrix.to_excel(OUTPUT_FILE, index=False)
    except Exception as exc:
        logging.exception("Erreur lors de l'ecriture du fichier: %s", exc)
        sys.exit(1)

    logging.info("Matrice finale géneree: %s", OUTPUT_FILE)
    sys.exit(0)


if __name__ == "__main__":
    main()
