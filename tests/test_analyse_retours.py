"""Tests for the feedback impact analysis script."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import scripts.analyse_retours as ar


def test_compute_impact_summary(tmp_path: Path) -> None:
    """Ensure ``compute_impact`` aggregates criticity correctly."""
    df = pd.DataFrame({"Criticité": ["Haute", "Basse", "Haute"]})
    file_path = tmp_path / "retours.xlsx"
    df.to_excel(file_path, index=False, engine="openpyxl")

    report = ar.compute_impact(file_path)
    assert report.loc[report["Criticite"] == "haute", "Occurrences"].iat[0] == 2
    assert report.iloc[-1]["Criticite"] == "Score global"


def test_main_creates_report(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """``main`` should create the CSV report and exit with code ``0``."""
    df = pd.DataFrame({"Criticité": ["Haute"]})
    input_file = tmp_path / "retours.xlsx"
    df.to_excel(input_file, index=False, engine="openpyxl")
    output_file = tmp_path / "impact.csv"
    log_file = tmp_path / "log.log"

    monkeypatch.setattr(ar, "DATA_FILE", input_file)
    monkeypatch.setattr(ar, "REPORT_FILE", output_file)
    monkeypatch.setattr(ar, "LOG_FILE", log_file)

    with pytest.raises(SystemExit) as exc:
        ar.main()
    assert exc.value.code == 0
    assert output_file.exists()


def test_main_missing_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """``main`` exits with code ``1`` when the input file is absent."""
    monkeypatch.setattr(ar, "DATA_FILE", tmp_path / "absent.xlsx")
    monkeypatch.setattr(ar, "REPORT_FILE", tmp_path / "impact.csv")
    monkeypatch.setattr(ar, "LOG_FILE", tmp_path / "log.log")

    with pytest.raises(SystemExit) as exc:
        ar.main()
    assert exc.value.code == 1
