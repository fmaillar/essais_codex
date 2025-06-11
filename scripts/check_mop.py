"""Validate presence of MOP for applicable requirements."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

LOG_FILE = Path("logs/check_mop.log")
AUDIT_FILE = Path("audit/mop_manquants.csv")
DATA_FILE = Path("data/mop.xlsx")


def setup_logger() -> None:
    """Configure logging."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def check_mop(filepath: Path) -> pd.DataFrame:
    """Return rows with missing MOP."""
    df = pd.read_excel(filepath, engine="openpyxl")
    mask = (df.get("Applicability") == "Oui") & (df.get("MOP").isna())
    return df.loc[mask]


def main() -> None:
    """Script entry point."""
    setup_logger()

    if not DATA_FILE.exists():
        logging.error("Fichier %s introuvable", DATA_FILE)
        sys.exit(1)

    try:
        invalid_rows = check_mop(DATA_FILE)
    except Exception as exc:
        logging.exception("Erreur lors de la lecture du fichier: %s", exc)
        sys.exit(1)

    if not invalid_rows.empty:
        AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
        invalid_rows.to_csv(AUDIT_FILE, index=False)
        logging.warning("MOP manquants: %d", len(invalid_rows))
        sys.exit(1)

    logging.info("Tous les MOP sont renseignes")
    sys.exit(0)


if __name__ == "__main__":
    main()
