"""Check requirement completeness for the certification workflow.

The script implements step ``check_exigences`` defined in
``workflow_certif.yaml``. It reads ``data/exigences.xlsx`` and exports all
non-conforming rows to ``audit/exigences_incompletes.csv``.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

LOG_FILE = Path("logs/check_exigences.log")
AUDIT_FILE = Path("audit/exigences_incompletes.csv")
DATA_FILE = Path("data/exigences.xlsx")


def setup_logger() -> None:
    """Configure file-based logging.

    Returns
    -------
    None
        This function only configures the logger.
    """
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def verify_exigences(filepath: Path) -> pd.DataFrame:
    """Return non-conforming rows from the requirements file.

    Parameters
    ----------
    filepath : Path
        Path to the Excel file containing the requirements.

    Returns
    -------
    pandas.DataFrame
        DataFrame of rows where applicability is ``Oui`` and justification is
        missing.
    """
    df = pd.read_excel(filepath, engine="openpyxl")
    mask = (
        df.get("Applicability") == "Oui"
    ) & (df.get("Justification non-applicabilité").isna())
    return df.loc[mask]


def main() -> None:
    """Execute requirement checks and export inconsistencies.

    Returns
    -------
    None
        Exits the program with status code ``0`` or ``1``.
    """
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
        AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
        invalid_rows.to_csv(AUDIT_FILE, index=False)
        logging.warning(
            "Exigences non conformes detectees: %d", len(invalid_rows)
        )
        sys.exit(1)

    logging.info("Aucune anomalie detectee")
    sys.exit(0)


if __name__ == "__main__":
    main()
