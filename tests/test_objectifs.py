from pathlib import Path
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core import ObjectifManager
from workflow import WorkflowCertifEngine, CertificationDossier
from workflow.steps import EtapeWorkflow


class DummyStep(EtapeWorkflow):
    """Step always succeeding."""

    def executer(self, dossier: CertificationDossier) -> bool:
        return True


def test_objectif_manager(tmp_path: Path) -> None:
    yaml_file = tmp_path / "obj.yaml"
    yaml_file.write_text(
        """
- id: OBJ
  nom: Test
  description: test
  preconditions: [dummy]
  actions: [dummy]
  criticite: basse
""",
        encoding="utf-8",
    )

    engine = WorkflowCertifEngine()
    step = DummyStep(None)
    engine.etapes_dict = {"dummy": step}

    dossier_dir = tmp_path / "dossier"
    dossier_dir.mkdir()
    dossier = CertificationDossier("ID", dossier_dir)

    manager = ObjectifManager()
    manager.charger_yaml(yaml_file)
    manager.declencher(engine, dossier)

    assert manager.objectifs["OBJ"].statut == "atteint"
