"""Reporting helpers for the certification workflow."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd


@dataclass
class RapportImpact:
    """Container for impact reports."""

    contenu: pd.DataFrame = field(default_factory=pd.DataFrame)

    def generer(self, df: pd.DataFrame) -> None:
        """Load impact ``df`` into the report."""
        self.contenu = df

    def exporter_csv(self, path: Path) -> None:
        """Export the report to ``path`` in CSV format."""
        path.parent.mkdir(parents=True, exist_ok=True)
        self.contenu.to_csv(path, index=False)
