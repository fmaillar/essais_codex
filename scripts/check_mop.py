"""Check the presence of MOP for each applicable requirement."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

from .utils import DEFAULT_SHEETS, find_column, read_first_sheet

LOG_FILE = Path("logs/check_mop.log")
AUDIT_FILE = Path("audit/mop_manquants.csv")
DATA_FILE = Path("data/mop.xlsx")


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


def check_mop(filepath: Path) -> pd.DataFrame:
    """Return rows with missing MOP.

    Parameters
    ----------
    filepath : Path
        Path to the Excel file describing the MOP.

    Returns
    -------
    pandas.DataFrame
        DataFrame of requirements lacking a MOP.
    """
    df = read_first_sheet(filepath, DEFAULT_SHEETS)

    try:
        app_col = find_column(
            df,
            [r"^Applicabilit[ée]$", r"^Applicability$"],
            [r"applicab"],
        )
        mop_col = find_column(df, [r"^MOP$"], [r"moyen.*preuve"])
    except KeyError as exc:
        raise KeyError(f"Colonnes manquantes: {exc}") from exc

    mask = (df[app_col].str.lower() == "oui") & df[mop_col].isna()
    return df.loc[mask]


def main() -> None:
    """Validate MOP presence and export missing entries.

    Returns
    -------
    None
        Exits with status code ``0`` or ``1`` depending on the result.
    """
    setup_logger()

    if not DATA_FILE.exists():
        logging.error("Fichier %s introuvable", DATA_FILE)
        sys.exit(1)

    logging.info("Lecture du fichier: %s", DATA_FILE)
    try:
        invalid_rows = check_mop(DATA_FILE)
    except KeyError as exc:
        logging.error("%s", exc)
        sys.exit(1)
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
