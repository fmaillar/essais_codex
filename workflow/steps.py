"""Workflow step implementations."""

from __future__ import annotations

import subprocess
from pathlib import Path
from abc import ABC, abstractmethod

from .models import CertificationDossier
from .logger import LoggerCertif


class EtapeWorkflow(ABC):
    """Base class for workflow steps."""

    def __init__(self, script: Path | None = None) -> None:
        self.script = script
        self.logger = LoggerCertif()

    @abstractmethod
    def executer(self, dossier: CertificationDossier) -> bool:
        """Run the step on ``dossier``."""
        raise NotImplementedError


class ScriptStep(EtapeWorkflow):
    """Generic step executing an external Python script."""

    def executer(self, dossier: CertificationDossier) -> bool:
        if not self.script:
            self.logger.log_info("Aucun script a executer")
            return True
        result = subprocess.run(["python", str(self.script)], capture_output=True, text=True)
        if result.returncode != 0:
            self.logger.log_error(result.stderr)
        else:
            self.logger.log_info(result.stdout)
        return result.returncode == 0


class CheckPreuves(ScriptStep):
    """Step verifying evidences."""


class AnalyseRetours(ScriptStep):
    """Step analysing evaluator feedback."""


class CheckMOP(ScriptStep):
    """Step validating MOP presence."""


class SoumettreDossier(ScriptStep):
    """Step submitting the dossier."""


class CheckExigences(ScriptStep):
    """Step verifying documentary requirements."""


class GererRetours(ScriptStep):
    """Step handling evaluator feedback."""
