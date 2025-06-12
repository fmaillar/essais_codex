from pathlib import Path
from core.workflow_engine import WorkflowCertifEngine
from core.etapes import (
    CheckExigencesStep,
    CheckMOPStep,
    CheckPreuvesStep,
    SoumettreDossierStep,
    GererRetoursStep,
)


def test_engine_steps() -> None:
    mapping = {
        "check_exigences": CheckExigencesStep,
        "check_mop": CheckMOPStep,
        "check_preuves": CheckPreuvesStep,
        "soumettre_dossier": SoumettreDossierStep,
        "gerer_retours": GererRetoursStep,
    }
    engine = WorkflowCertifEngine.from_yaml(Path("workflow_certif.yaml"), mapping)
    assert len(engine.steps) == 5

