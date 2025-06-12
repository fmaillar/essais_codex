"""Engine orchestrating certification workflow steps."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Type

import yaml

from .certification_dossier import CertificationDossier

logger = logging.getLogger(__name__)


class EtapeWorkflow(ABC):
    """Abstract base class for workflow steps."""

    id: str

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    @abstractmethod
    def run(self, dossier: CertificationDossier) -> bool:
        """Execute the step and return ``True`` on success."""


class WorkflowCertifEngine:
    """Load steps from YAML and execute them sequentially."""

    def __init__(self, dossier: CertificationDossier, steps: List[EtapeWorkflow]):
        self.dossier = dossier
        self.steps = steps

    @classmethod
    def from_yaml(cls, yaml_path: Path, step_map: Dict[str, Type[EtapeWorkflow]]) -> "WorkflowCertifEngine":
        """Instantiate the engine from a YAML configuration."""
        with yaml_path.open("r", encoding="utf-8") as fh:
            cfg = yaml.safe_load(fh)

        dossier = CertificationDossier(
            Path(cfg.get("data_folder", "data")),
            Path(cfg.get("audit_folder", "audit")),
            Path(cfg.get("log_folder", "logs")),
        )

        steps_cfg = cfg.get("steps", [])
        steps: List[EtapeWorkflow] = []
        for scfg in steps_cfg:
            sid = scfg.get("id")
            step_cls = step_map.get(sid)
            if not step_cls:
                logger.warning("Étape %s inconnue, ignorée", sid)
                continue
            steps.append(step_cls(scfg))

        return cls(dossier, steps)

    def run(self) -> int:
        """Run every configured step."""
        for step in self.steps:
            logger.info("Exécution de l'étape %s", step.config.get("id"))
            if not step.run(self.dossier):
                logger.error("Échec de l'étape %s", step.config.get("id"))
                return 1
        return 0
