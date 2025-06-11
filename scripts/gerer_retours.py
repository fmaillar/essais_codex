"""Process evaluator feedback and log critical issues."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

LOG_FILE = Path("logs/gerer_retours.log")
AUDIT_FILE = Path("audit/retours_critiques.csv")
SUMMARY_FILE = Path("audit/retours_traite_nontraite.csv")
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


def extract_critiques(filepath: Path) -> pd.DataFrame:
    """Return critical feedback lines.

    Parameters
    ----------
    filepath : Path
        Path to the Excel file with evaluator feedback.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing only lines flagged as critical.
    """
    df = pd.read_excel(filepath, engine="openpyxl")
    mask = df.get("Criticité", "").str.lower() == "elevee"
    return df.loc[mask]


def update_traitement(filepath: Path) -> pd.DataFrame:
    """Update feedback file with a ``Traité`` column and return summary.

    Parameters
    ----------
    filepath : Path
        Path to the Excel file with evaluator feedback.

    Returns
    -------
    pandas.DataFrame
        Counts of treated vs non-treated comments.
    """
    df = pd.read_excel(filepath, engine="openpyxl")

    comment_col = df.filter(regex="(?i)comment").columns[0]
    keywords = r"(résolu|corrigé|pris en compte)"

    df["Traité"] = df[comment_col].str.contains(keywords, case=False, na=False)
    df["Traité"] = df["Traité"].map({True: "Oui", False: "Non"})

    df.to_excel(filepath, index=False, engine="openpyxl")
    return df["Traité"].value_counts().rename_axis("Traite").reset_index(name="Occurrences")


def main() -> None:
    """Process feedback and export audit files.

    Returns
    -------
    None
        Exits with status ``0`` or ``1`` depending on the feedback severity.
    """
    setup_logger()

    if not DATA_FILE.exists():
        logging.error("Fichier %s introuvable", DATA_FILE)
        sys.exit(1)

    try:
        critiques = extract_critiques(DATA_FILE)
        summary = update_traitement(DATA_FILE)
    except Exception as exc:
        logging.exception("Erreur de lecture des retours: %s", exc)
        sys.exit(1)

    SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(SUMMARY_FILE, index=False)

    if not critiques.empty:
        AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
        critiques.to_csv(AUDIT_FILE, index=False)
        logging.warning("Retours critiques identifies: %d", len(critiques))
        sys.exit(1)

    logging.info("Aucun retour critique")
    sys.exit(0)


if __name__ == "__main__":
    main()
