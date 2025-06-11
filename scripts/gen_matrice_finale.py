"""Generate the consolidated certification matrix."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

from .utils import DEFAULT_SHEETS, find_column, read_first_sheet

LOG_FILE = Path("logs/gen_matrice_finale.log")
OUTPUT_FILE = Path("audit/matrice_finale.xlsx")
EVIDENCE_FILE = Path("data/preuves.xlsx")


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


def generate_matrix(filepath: Path) -> pd.DataFrame:
    """Return compliant evidence rows from the Excel file.

    Parameters
    ----------
    filepath : Path
        Path to the evidence Excel file.

    Returns
    -------
    pandas.DataFrame
        Filtered DataFrame containing only valid entries.
    """
    df = read_first_sheet(filepath, DEFAULT_SHEETS)

    applicability_col = find_column(df, [r"^Applicabilit[ée]$", r"^Applicability$"], [r"applicab"])
    design_col = find_column(df, [r"preuve.*conception"], [r"preuve.*conc"])
    test_col = find_column(df, [r"preuve.*test"], None)

    mask = (
        df[applicability_col].str.lower() == "oui"
    ) & df[design_col].notna() & df[test_col].notna()

    return df.loc[mask]


def main() -> None:
    """Generate the final matrix and export it.

    Returns
    -------
    None
        Exits with ``0`` on success, ``1`` on failure.
    """
    setup_logger()

    if not EVIDENCE_FILE.exists():
        logging.error("Fichier %s introuvable", EVIDENCE_FILE)
        sys.exit(1)

    logging.info("Lecture du fichier: %s", EVIDENCE_FILE)
    try:
        matrix = generate_matrix(EVIDENCE_FILE)
    except KeyError as exc:
        logging.error("%s", exc)
        sys.exit(1)
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
