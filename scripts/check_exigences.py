"""Check requirements applicability and justification."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

LOG_FILE = Path("logs/check_exigences.log")
AUDIT_FILE = Path("audit/exigences_incompletes.csv")
DATA_FILE = Path("data/exigences.xlsx")


def setup_logger() -> None:
    """Configure logging to file."""
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def verify_exigences(filepath: Path) -> pd.DataFrame:
    """Return non conforming rows from the requirements file."""
    df = pd.read_excel(filepath, engine="openpyxl")
    mask = (df.get("Applicability") == "Oui") & (df.get("Justification non-applicabilité").isna())
    return df.loc[mask]


def main() -> None:
    """Entry point for the script."""
    setup_logger()

    if not DATA_FILE.exists():
        logging.error("Fichier %s introuvable", DATA_FILE)
        sys.exit(1)

    try:
        invalid_rows = verify_exigences(DATA_FILE)
    except Exception as exc:  # fallback for unexpected format
        logging.exception("Erreur lors de la lecture du fichier: %s", exc)
        sys.exit(1)

    if not invalid_rows.empty:
        invalid_rows.to_csv(AUDIT_FILE, index=False)
        logging.warning("Exigences non conformes detectees: %d", len(invalid_rows))
        sys.exit(1)

    logging.info("Aucune anomalie detectee")
    sys.exit(0)


if __name__ == "__main__":
    main()
