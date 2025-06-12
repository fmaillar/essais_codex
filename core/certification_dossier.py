"""Core data container for the certification workflow."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd

from scripts.utils import read_first_sheet

logger = logging.getLogger(__name__)


@dataclass
class CertificationDossier:
    """Represent a project dossier with input and output folders."""

    data_dir: Path
    audit_dir: Path
    log_dir: Path

    def data_path(self, name: str) -> Path:
        """Return the path to a data file and ensure it exists."""
        path = self.data_dir / name
        if not path.exists():
            raise FileNotFoundError(f"Fichier introuvable: {path}")
        return path

    def audit_path(self, name: str) -> Path:
        """Return the path to an audit file creating directories if needed."""
        path = self.audit_dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def log_path(self, name: str) -> Path:
        """Return the path to a log file creating directories if needed."""
        path = self.log_dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def read_excel(self, filename: str, sheets: Iterable[str] | None = None) -> pd.DataFrame:
        """Load an Excel file from the data directory."""
        file_path = self.data_path(filename)
        logger.info("Lecture du fichier Excel %s", file_path)
        return read_first_sheet(file_path, sheets)

    def save_csv(self, df: pd.DataFrame, filename: str) -> None:
        """Save a DataFrame to the audit directory."""
        path = self.audit_path(filename)
        df.to_csv(path, index=False)
        logger.info("Fichier CSV sauvegarde: %s", path)
