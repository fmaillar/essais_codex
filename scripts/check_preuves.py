"""Validate design and test evidence for each applicable requirement."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

LOG_FILE = Path("logs/check_preuves.log")
AUDIT_FILE = Path("audit/preuves_manquantes.csv")
EXIG_AUDIT_FILE = Path("audit/exigences_sans_preuves.csv")
PREUVES_FILE = Path("data/preuves.xlsx")
EXIG_FILE = Path("data/exigences.xlsx")


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


def check_preuves(filepath: Path) -> pd.DataFrame:
    """Return rows missing design or test evidence.

    Parameters
    ----------
    filepath : Path
        Path to the Excel file listing evidence.

    Returns
    -------
    pandas.DataFrame
        DataFrame of requirements missing either design or test evidence.
    """
    df = pd.read_excel(filepath, engine="openpyxl")

    applicability_col = df.filter(regex="(?i)applicab").columns
    if not applicability_col.empty:
        applicability_col = applicability_col[0]
    else:  # fallback when column absent
        applicability_col = None

    design_col = df.filter(regex="(?i)preuve.*conc").columns[0]
    test_col = df.filter(regex="(?i)preuve.*test").columns[0]

    mask = df[design_col].isna() | df[test_col].isna()
    if applicability_col:
        mask &= df[applicability_col].str.lower() == "oui"
    return df.loc[mask]


def exigences_sans_preuves(
    exig_path: Path, preuves_path: Path
) -> pd.DataFrame:
    """Return requirements with no design or test evidence.

    Parameters
    ----------
    exig_path : Path
        Path to the Excel file containing requirements.
    preuves_path : Path
        Path to the Excel file containing evidence.

    Returns
    -------
    pandas.DataFrame
        DataFrame listing requirement identifiers without associated evidence.
    """
    df_exig = pd.read_excel(exig_path, engine="openpyxl")
    df_preuves = pd.read_excel(preuves_path, engine="openpyxl")

    id_exig = df_exig.filter(regex="(?i)id|exig").columns[0]
    id_prev = df_preuves.filter(regex="(?i)id|exig").columns[0]
    design_col = df_preuves.filter(regex="(?i)preuve.*conc").columns[0]
    test_col = df_preuves.filter(regex="(?i)preuve.*test").columns[0]

    merged = df_exig[[id_exig]].merge(
        df_preuves[[id_prev, design_col, test_col]],
        how="left",
        left_on=id_exig,
        right_on=id_prev,
    )

    mask = merged[design_col].isna() & merged[test_col].isna()
    return merged.loc[mask, [id_exig]]


def main() -> None:
    """Check evidence files and export missing information.

    Returns
    -------
    None
        Exits with status ``0`` if everything is present, ``1`` otherwise.
    """
    setup_logger()

    for path in (PREUVES_FILE, EXIG_FILE):
        if not path.exists():
            logging.error("Fichier %s introuvable", path)
            sys.exit(1)

    try:
        invalid_rows = check_preuves(PREUVES_FILE)
        missing_exig = exigences_sans_preuves(EXIG_FILE, PREUVES_FILE)
    except Exception as exc:
        logging.exception("Erreur lors de la lecture du fichier: %s", exc)
        sys.exit(1)

    if not invalid_rows.empty:
        AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
        invalid_rows.to_csv(AUDIT_FILE, index=False)
        logging.warning("Preuves manquantes: %d", len(invalid_rows))

    if not missing_exig.empty:
        EXIG_AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
        missing_exig.to_csv(EXIG_AUDIT_FILE, index=False)
        logging.warning(
            "Exigences sans preuve associee: %d", len(missing_exig)
        )

    if not invalid_rows.empty or not missing_exig.empty:
        sys.exit(1)

    logging.info("Toutes les preuves sont presentes")
    sys.exit(0)


if __name__ == "__main__":
    main()
