import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pandas as pd
from pathlib import Path

from scripts.gen_matrice_finale import generate_matrix
from scripts.analyse_retours import compute_impact


def test_generate_matrix(tmp_path: Path) -> None:
    df = pd.DataFrame({
        "Applicability": ["Oui", "Non", "Oui"],
        "Preuve_conception": ["doc1", None, "doc2"],
        "Preuve_test": ["test1", "test2", None],
    })
    file_path = tmp_path / "preuves.xlsx"
    df.to_excel(file_path, index=False, engine="openpyxl")

    result = generate_matrix(file_path)
    assert len(result) == 1


def test_compute_impact(tmp_path: Path) -> None:
    df = pd.DataFrame({"Criticité": ["Élevée", "Faible", "Élevée"]})
    file_path = tmp_path / "retours.xlsx"
    df.to_excel(file_path, index=False, engine="openpyxl")

    report = compute_impact(file_path)
    assert report.loc[report["Criticite"] == "élevée", "Occurrences"].iat[0] == 2
    assert "Poids" in report.columns
    assert report.iloc[-1]["Criticite"] == "Score global"

