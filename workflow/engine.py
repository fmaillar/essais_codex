"""Workflow engine orchestrating the certification steps."""

from __future__ import annotations

from pathlib import Path
from typing import Any, List

import yaml

from .models import CertificationDossier
from .steps import (
    EtapeWorkflow,
    CheckExigences,
    CheckMOP,
    CheckPreuves,
    SoumettreDossier,
    AnalyseRetours,
    GererRetours,
    ScriptStep,
)


class WorkflowCertifEngine:
    """Load and run certification steps defined in a YAML file."""

    def __init__(self) -> None:
        self.etapes: List[EtapeWorkflow] = []
        self.etapes_dict: dict[str, EtapeWorkflow] = {}
        self.objectifs: dict[str, Any] = {}

    def charger_workflow(self, yaml_path: Path) -> None:
        """Populate ``self.etapes`` from ``yaml_path``."""
        with yaml_path.open("r", encoding="utf-8") as fh:
            config = yaml.safe_load(fh)
        mapping = {
            "check_exigences": CheckExigences,
            "check_mop": CheckMOP,
            "check_preuves": CheckPreuves,
            "soumettre_dossier": SoumettreDossier,
            "gerer_retours": GererRetours,
            "analyse_retours": AnalyseRetours,
        }
        self.etapes = []
        self.etapes_dict = {}
        for step_cfg in config.get("steps", []):
            step_cls = mapping.get(step_cfg["id"], ScriptStep)
            script = Path(step_cfg.get("script", "")) if step_cfg.get("script") else None
            instance = step_cls(script)
            self.etapes.append(instance)
            self.etapes_dict[step_cfg["id"]] = instance

    def charger_objectifs(self, yaml_path: Path) -> None:
        """Load objectives definition from ``yaml_path``."""
        with yaml_path.open("r", encoding="utf-8") as fh:
            self.objectifs = yaml.safe_load(fh)

    def atteindre_objectif(self, nom: str, dossier: CertificationDossier) -> None:
        """Execute steps required to reach ``nom``."""
        obj = self.objectifs.get("objectifs", {}).get(nom)
        if not obj:
            raise ValueError(f"Objectif inconnu: {nom}")
        steps = obj.get("preconditions", [])
        for step_id in steps:
            step = self.etapes_dict.get(step_id)
            if not step:
                continue
            if not step.executer(dossier):
                dossier.statut = "echec"
                dossier.sauvegarder_statut()
                raise RuntimeError(f"Étape échouée: {step_id}")
        if self.verifier_conditions_succes(obj.get("conditions_succès", [])):
            dossier.statut = "termine"
        else:
            dossier.statut = "incomplet"
        dossier.sauvegarder_statut()

    def verifier_conditions_succes(self, conditions: list[dict[str, Any]]) -> bool:
        """Return ``True`` if all ``conditions`` are satisfied."""
        for cond in conditions:
            path = Path(cond.get("fichier", ""))
            if cond.get("existe") and not path.exists():
                return False
        return True

    def evaluer_progres(self, objectif: str) -> float:
        """Return completion ratio for ``objectif``."""
        obj = self.objectifs.get("objectifs", {}).get(objectif, {})
        steps = obj.get("preconditions", [])
        if not steps:
            return 0.0
        done = sum(1 for s in steps if s in self.etapes_dict)
        return done / len(steps)

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
