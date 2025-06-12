from pathlib import Path
import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(ROOT, "src"))
sys.path.append(ROOT)

from workflow_certif import CertificationDossier, WorkflowCertifEngine


def test_engine_load_and_run(tmp_path: Path) -> None:
    yaml_path = Path('workflow_certif.yaml')
    engine = WorkflowCertifEngine()
    engine.charger_workflow(yaml_path)
    assert len(engine.etapes) == 5

    dossier_dir = tmp_path / 'dossier'
    dossier_dir.mkdir()
    dossier = CertificationDossier('TEST', dossier_dir)
    # run steps; they will likely fail due to missing scripts but should raise RuntimeError
    try:
        engine.lancer(dossier)
    except RuntimeError:
        assert dossier.statut == 'echec'
    else:
        assert dossier.statut == 'termine'
