"""Tests for generating a synthesis workbook from evaluator feedback."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from scripts.synthese_retours import synthese_retours


def test_synthese_retours_generate(tmp_path: Path) -> None:
    """The Excel workbook should contain both expected sheets."""
    df = pd.DataFrame({
        "Exigence": ["REQ1", "REQ1", "REQ2"],
        "Commentaire": ["C1", "C2", "C3"],
        "Criticité": ["Haute", "Basse", "Moyenne"],
    })
    input_file = tmp_path / "retours.xlsx"
    df.to_excel(input_file, index=False, engine="openpyxl")
    output_file = tmp_path / "synthese.xlsx"

    synthese_retours(input_file, output_file)

    assert output_file.exists()
    sheets = pd.read_excel(output_file, sheet_name=None, engine="openpyxl")
    assert set(sheets.keys()) == {"Tous_Retours", "Synthèse"}
    assert len(sheets["Tous_Retours"]) == 3
    row = sheets["Synthèse"].loc[sheets["Synthèse"]["Exigence"] == "REQ1"].iloc[0]
    assert row["Commentaire"] == "C1 | C2"


def test_synthese_retours_missing_columns(tmp_path: Path) -> None:
    """Missing expected columns must raise ``ValueError``."""
    df = pd.DataFrame({"Exigence": ["REQ1"], "Comment": ["C"]})
    input_file = tmp_path / "retours.xlsx"
    df.to_excel(input_file, index=False, engine="openpyxl")
    output_file = tmp_path / "out.xlsx"

    with pytest.raises(ValueError):
        synthese_retours(input_file, output_file)
