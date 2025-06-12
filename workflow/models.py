"""Data models for the certification workflow."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from .reporting import RapportImpact
from .logger import LoggerCertif


@dataclass
class CertificationDossier:
    """Represent a certification dossier.

    Parameters
    ----------
    id : str
        Identifier of the dossier.
    chemin_dossier : Path
        Root directory containing the certification files.
    statut : str
        Current workflow status.
    """

    id: str
    chemin_dossier: Path
    statut: str = "en_preparation"
    impact: RapportImpact | None = field(default=None, init=False)
    logger: LoggerCertif = field(default_factory=LoggerCertif, init=False)

    def charger_documents(self) -> None:
        """Load documents for the dossier.

        The implementation simply checks that the directory exists.
        """
        if not self.chemin_dossier.exists():
            self.logger.log_error(f"Dossier introuvable: {self.chemin_dossier}")
            raise FileNotFoundError(self.chemin_dossier)
        self.logger.log_info(f"Chargement du dossier: {self.chemin_dossier}")

    def sauvegarder_statut(self) -> None:
        """Persist the workflow status."""
        statut_file = self.chemin_dossier / "statut.txt"
        try:
            statut_file.write_text(self.statut, encoding="utf-8")
        except OSError as exc:
            self.logger.log_error(f"Erreur ecriture statut: {exc}")
            raise
        self.logger.log_info(f"Statut sauvegarde: {self.statut}")

    def enregistrer_impact(self, df: pd.DataFrame) -> None:
        """Store an impact report inside the dossier."""
        self.impact = RapportImpact(df)
        csv_path = self.chemin_dossier / "impact.csv"
        self.impact.exporter_csv(csv_path)
        self.logger.log_info(f"Rapport d'impact enregistre: {csv_path}")
