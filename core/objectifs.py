"""Objective management classes for the certification workflow."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List

import yaml

from workflow import CertificationDossier, WorkflowCertifEngine


@dataclass
class Objectif:
    """Represent a certification objective."""

    id: str
    description: str = ""
    preconditions: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    resultats_attendus: List[Dict[str, Any]] = field(default_factory=list)
    statut: str = field(default="non_declenche", init=False)

    def preconditions_ok(self, engine: WorkflowCertifEngine) -> bool:
        """Return ``True`` if every precondition is satisfied."""
        for pre in self.preconditions:
            if pre in engine.etapes_dict:
                continue
            if not Path(pre).exists():
                return False
        return True

    def executer(self, engine: WorkflowCertifEngine, dossier: CertificationDossier) -> bool:
        """Run objective actions through ``engine``."""
        self.statut = "en_cours"
        for act in self.actions:
            step = engine.etapes_dict.get(act)
            if not step:
                continue
            if not step.executer(dossier):
                self.statut = "bloque"
                return False
        if self.resultats_valides():
            self.statut = "atteint"
        else:
            self.statut = "bloque"
        return self.statut == "atteint"

    def resultats_valides(self) -> bool:
        """Check expected results presence."""
        for res in self.resultats_attendus:
            path = Path(res.get("fichier", ""))
            if res.get("existe") and not path.exists():
                return False
        return True

    @staticmethod
    def from_dict(identifier: str, data: Dict[str, Any]) -> "Objectif":
        """Create an ``Objectif`` instance from a mapping."""
        return Objectif(
            id=identifier,
            description=data.get("description", ""),
            preconditions=list(data.get("preconditions", [])),
            actions=list(data.get("actions", [])),
            resultats_attendus=list(data.get("resultats_attendus", [])),
        )


class ObjectifManager:
    """Manage a collection of :class:`Objectif` instances."""

    def __init__(self, log_file: Path | None = None) -> None:
        self.objectifs: Dict[str, Objectif] = {}
        log_file = log_file or Path("logs/objectifs.log")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self._logger = logging.getLogger("objectif_manager")

    def charger_yaml(self, yaml_path: Path) -> None:
        """Load objectives definitions from ``yaml_path``."""
        with yaml_path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        for ident, obj_data in (data.get("objectifs") or {}).items():
            self.objectifs[ident] = Objectif.from_dict(ident, obj_data)
        self._logger.info("%d objectifs charges", len(self.objectifs))

    def declencher(self, engine: WorkflowCertifEngine, dossier: CertificationDossier) -> None:
        """Trigger all objectives sequentially."""
        for obj in self.objectifs.values():
            if not obj.preconditions_ok(engine):
                obj.statut = "bloque"
                self._logger.warning("Preconditions manquantes pour %s", obj.id)
                continue
            self._logger.info("Execution objectif %s", obj.id)
            obj.executer(engine, dossier)
            self._logger.info("Statut %s: %s", obj.id, obj.statut)

    def rapport(self) -> str:
        """Return a synthetic status report."""
        lines = [f"{o.id}: {o.statut}" for o in self.objectifs.values()]
        return "\n".join(lines)


def objectif(identifier: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator linking a function to an ``Objectif`` identifier."""

    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        setattr(func, "__objectif_id__", identifier)
        return func

    return wrapper
