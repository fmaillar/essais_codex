"""Analyse les retours des évaluateurs et génère un rapport d'impact."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

LOG_FILE = Path("logs/analyse_retours.log")
REPORT_FILE = Path("audit/impact_retours.csv")
DATA_FILE = Path("data/retours.xlsx")


def setup_logger() -> None:
    """Configure file based logging."""
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def compute_impact(filepath: Path) -> pd.DataFrame:
    """Return feedback impact summary grouped by criticity level.

    Parameters
    ----------
    filepath : Path
        Excel file path containing evaluator feedback.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ``Criticite`` and ``Occurrences``.
    """
    df = pd.read_excel(filepath, engine="openpyxl")

    criticity_col = df.filter(regex="(?i)critic").columns[0]
    counts = (
        df[criticity_col].str.lower().value_counts().rename_axis("Criticite")
    )
    return counts.rename("Occurrences").reset_index()


def main() -> None:
    """Analyse feedback and export an impact report."""
    setup_logger()

    if not DATA_FILE.exists():
        logging.error("Fichier %s introuvable", DATA_FILE)
        sys.exit(1)

    try:
        report = compute_impact(DATA_FILE)
    except Exception as exc:  # fallback for unexpected format
        logging.exception("Erreur lors de l'analyse des retours: %s", exc)
        sys.exit(1)

    try:
        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
        report.to_csv(REPORT_FILE, index=False)
    except Exception as exc:
        logging.exception("Erreur lors de l'ecriture du rapport: %s", exc)
        sys.exit(1)

    logging.info("Rapport d'impact genere: %s", REPORT_FILE)
    sys.exit(0)


if __name__ == "__main__":
    main()
