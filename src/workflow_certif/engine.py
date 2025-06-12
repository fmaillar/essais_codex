"""Workflow engine orchestrating the certification steps."""

from __future__ import annotations

from pathlib import Path
from typing import List

import yaml

from .models import CertificationDossier
from .steps import (
    EtapeWorkflow,
    VerificationPreuves,
    AnalyseRetours,
    ValidationMOP,
    SoumissionDossier,
    ScriptStep,
)


class WorkflowCertifEngine:
    """Load and run certification steps defined in a YAML file."""

    def __init__(self) -> None:
        self.etapes: List[EtapeWorkflow] = []

    def charger_workflow(self, yaml_path: Path) -> None:
        """Populate ``self.etapes`` from ``yaml_path``."""
        with yaml_path.open("r", encoding="utf-8") as fh:
            config = yaml.safe_load(fh)
        mapping = {
            "check_preuves": VerificationPreuves,
            "gerer_retours": AnalyseRetours,
            "check_mop": ValidationMOP,
            "soumettre_dossier": SoumissionDossier,
        }
        self.etapes = []
        for step_cfg in config.get("steps", []):
            step_cls = mapping.get(step_cfg["id"], ScriptStep)
            script = Path(step_cfg.get("script", "")) if step_cfg.get("script") else None
            self.etapes.append(step_cls(script))

    def lancer(self, dossier: CertificationDossier) -> None:
        """Run all loaded steps sequentially."""
        for etape in self.etapes:
            ok = etape.executer(dossier)
            if not ok:
                dossier.statut = "echec"
                dossier.sauvegarder_statut()
                raise RuntimeError("Étape échouée")
        dossier.statut = "termine"
        dossier.sauvegarder_statut()
