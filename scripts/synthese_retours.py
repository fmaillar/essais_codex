"""Produce a summarized view of evaluator feedback."""

import logging
from pathlib import Path

import pandas as pd

from .utils import DEFAULT_SHEETS, find_column, read_first_sheet

LOG_FILE = Path("logs/synthese_retours.log")


def setup_logger() -> None:
    """Configure file-based logging."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def synthese_retours(input_path: Path, output_path: Path) -> None:
    """Generate a synthesis workbook from evaluator feedback.

    Parameters
    ----------
    input_path : Path
        Excel file containing raw feedback.
    output_path : Path
        Destination of the synthesized Excel file.

    Returns
    -------
    None
        The synthesized Excel file is written to ``output_path``.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Fichier introuvable: {input_path}")

    logging.info("Lecture du fichier: %s", input_path)

    df = read_first_sheet(input_path, DEFAULT_SHEETS)

    try:
        requirement_col = find_column(df, [r"^Exigence$"], [r"exig"])
        comment_col = find_column(df, [r"^Commentaire$"], [r"comment"])
        criticity_col = find_column(df, [r"^Criticité$"], [r"critic"])
    except KeyError as exc:
        raise ValueError(str(exc)) from exc

    required_cols = {requirement_col, comment_col, criticity_col}
    if not required_cols.issubset(df.columns):
        raise ValueError(
            f"Colonnes attendues manquantes dans le fichier : {required_cols}"
        )

    grouped = (
        df.groupby(requirement_col).agg(
            {
                comment_col: lambda x: " | ".join(x),
                criticity_col: lambda x: ", ".join(x),
            }
        )
        .reset_index()
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Tous_Retours", index=False)
        grouped.to_excel(writer, sheet_name="Synthèse", index=False)

    logging.info("Synthèse générée: %s", output_path)


if __name__ == "__main__":
    setup_logger()
    synthese_retours(Path("data/retours.xlsx"), Path("audit/synthese_retours.xlsx"))
