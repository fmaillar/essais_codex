import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pandas as pd
from pathlib import Path

from scripts.gen_matrice_finale import generate_matrix
from scripts.analyse_retours import compute_impact
from scripts.check_preuves import check_preuves, exigences_sans_preuves
from scripts.check_mop import check_mop
from scripts.check_exigences import verify_exigences


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


def test_check_preuves(tmp_path: Path) -> None:
    df = pd.DataFrame({
        "Applicabilité": ["Oui", "Oui"],
        "Preuve_conception": [None, "doc"],
        "Preuve_test": ["t1", None],
    })
    file_path = tmp_path / "preuves.xlsx"
    df.to_excel(file_path, index=False, engine="openpyxl")

    result = check_preuves(file_path)
    assert len(result) == 2


def test_exigences_sans_preuves(tmp_path: Path) -> None:
    df_exig = pd.DataFrame({"ID": ["REQ1", "REQ2"]})
    df_prev = pd.DataFrame({
        "ID": ["REQ1"],
        "Preuve_conception": ["doc"],
        "Preuve_test": [None],
    })
    p1 = tmp_path / "exig.xlsx"
    p2 = tmp_path / "prev.xlsx"
    df_exig.to_excel(p1, index=False, engine="openpyxl")
    df_prev.to_excel(p2, index=False, engine="openpyxl")

    missing = exigences_sans_preuves(p1, p2)
    assert len(missing) == 1


def test_check_mop(tmp_path: Path) -> None:
    df = pd.DataFrame({
        "Applicability": ["Oui", "Non"],
        "MOP": [None, "OK"],
    })
    file_path = tmp_path / "mop.xlsx"
    df.to_excel(file_path, index=False, engine="openpyxl")

    result = check_mop(file_path)
    assert len(result) == 1


def test_verify_exigences(tmp_path: Path) -> None:
    df = pd.DataFrame({
        "Applicability": ["Oui", "Non"],
        "Justification non-applicabilité": [None, ""],
    })
    file_path = tmp_path / "exig.xlsx"
    df.to_excel(file_path, index=False, engine="openpyxl")

    result = verify_exigences(file_path)
    assert len(result) == 1

