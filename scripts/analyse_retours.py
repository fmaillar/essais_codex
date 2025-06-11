"""Analyse les retours des évaluateurs et génère un rapport d'impact."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

from .utils import DEFAULT_SHEETS, find_column, read_first_sheet

LOG_FILE = Path("logs/analyse_retours.log")
REPORT_FILE = Path("audit/impact_retours.csv")
DATA_FILE = Path("data/retours.xlsx")


def setup_logger() -> None:
    """Configure file-based logging.

    Returns
    -------
    None
        The logger is configured for this module.
    """
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def compute_impact(filepath: Path) -> pd.DataFrame:
    """Return weighted impact summary from evaluator feedback.

    Parameters
    ----------
    filepath : Path
        Excel file path containing evaluator feedback.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns ``Criticite``, ``Occurrences`` and ``Poids`` with
        a final row ``Score global``.
    """
    df = read_first_sheet(filepath, DEFAULT_SHEETS)

    criticity_col = find_column(df, [r"^Criticité$"], [r"critic"])
    mapping = {"haute": 3, "moyenne": 2, "basse": 1}

    counts = (
        df[criticity_col].str.lower().value_counts().rename_axis("Criticite")
    )
    summary = counts.rename("Occurrences").reset_index()
    summary["Poids"] = summary["Criticite"].str.lower().map(mapping).fillna(0).astype(int)

    global_score = int(df[criticity_col].str.lower().map(mapping).fillna(0).sum())
    summary.loc[len(summary)] = ["Score global", global_score, ""]
    return summary


def main() -> None:
    """Analyse feedback and export an impact report.

    Returns
    -------
    None
        Exits with status ``0`` on success, ``1`` otherwise.
    """
    setup_logger()

    if not DATA_FILE.exists():
        logging.error("Fichier %s introuvable", DATA_FILE)
        sys.exit(1)

    logging.info("Lecture du fichier: %s", DATA_FILE)
    try:
        report = compute_impact(DATA_FILE)
    except KeyError as exc:
        logging.error("%s", exc)
        sys.exit(1)
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
