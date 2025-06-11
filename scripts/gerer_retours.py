"""Process evaluator feedback and log issues."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

LOG_FILE = Path("logs/gerer_retours.log")
AUDIT_FILE = Path("audit/retours_critiques.csv")
DATA_FILE = Path("data/retours.xlsx")


def setup_logger() -> None:
    """Configure logging."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def extract_critiques(filepath: Path) -> pd.DataFrame:
    """Return critical feedback lines."""
    df = pd.read_excel(filepath, engine="openpyxl")
    mask = df.get("Criticité", "").str.lower() == "elevee"
    return df.loc[mask]


def main() -> None:
    """Entry point."""
    setup_logger()

    if not DATA_FILE.exists():
        logging.error("Fichier %s introuvable", DATA_FILE)
        sys.exit(1)

    try:
        critiques = extract_critiques(DATA_FILE)
    except Exception as exc:
        logging.exception("Erreur de lecture des retours: %s", exc)
        sys.exit(1)

    if not critiques.empty:
        AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
        critiques.to_csv(AUDIT_FILE, index=False)
        logging.warning("Retours critiques identifies: %d", len(critiques))
        sys.exit(1)

    logging.info("Aucun retour critique")
    sys.exit(0)


if __name__ == "__main__":
    main()
