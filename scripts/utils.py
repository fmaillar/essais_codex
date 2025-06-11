"""Utility functions shared across workflow scripts."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable
import re

import pandas as pd


DEFAULT_SHEETS = ["Liste_documentaire", "Liste_Documentaire"]


def read_first_sheet(path: Path, sheets: Iterable[str] | None = None) -> pd.DataFrame:
    """Read the first matching sheet from an Excel file.

    Parameters
    ----------
    path : Path
        Excel file path.
    sheets : Iterable[str] | None
        Possible sheet names to search for. If ``None`` the first sheet is read.

    Returns
    -------
    pandas.DataFrame
        Data contained in the selected sheet.
    """
    xls = pd.ExcelFile(path, engine="openpyxl")
    if sheets:
        for sheet in sheets:
            if sheet in xls.sheet_names:
                logging.debug("Lecture de la feuille %s", sheet)
                return pd.read_excel(xls, sheet_name=sheet, engine="openpyxl")
    # fallback: first sheet
    logging.debug("Aucune feuille correspondante. Utilisation de la premiere.")
    return pd.read_excel(xls, sheet_name=0, engine="openpyxl")


def find_column(df: pd.DataFrame, patterns: Iterable[str], alt_patterns: Iterable[str] | None = None) -> str:
    """Return the first column name matching given patterns.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame where to search for the column.
    patterns : Iterable[str]
        Regex patterns to match exactly.
    alt_patterns : Iterable[str] | None
        Tolerant patterns used if no strict match is found.

    Returns
    -------
    str
        The matching column name.

    Raises
    ------
    KeyError
        If no column matches any of the provided patterns.
    """
    for pattern in patterns:
        regex = re.compile(pattern, flags=re.IGNORECASE)
        for col in df.columns:
            if regex.search(col):
                return col
    if alt_patterns:
        for pattern in alt_patterns:
            regex = re.compile(pattern, flags=re.IGNORECASE)
            for col in df.columns:
                if regex.search(col):
                    return col
    raise KeyError(f"Aucune colonne ne correspond aux motifs {list(patterns)}")
