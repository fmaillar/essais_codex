from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core import CertificationDossier, WorkflowCertifEngine
from core.etapes import SoumettreDossierStep


def test_dossier_missing_file(tmp_path: Path) -> None:
    dossier = CertificationDossier(tmp_path, tmp_path, tmp_path)
    with pytest.raises(FileNotFoundError):
        dossier.data_path("absent.xlsx")


def test_soumettre_dossier_step(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "f.txt").write_text("ok", encoding="utf-8")
    dossier = CertificationDossier(data_dir, tmp_path / "audit", tmp_path / "logs")
    step = SoumettreDossierStep({})
    assert step.run(dossier)
    assert (tmp_path / "audit" / "dossier_soumission.zip").exists()


def test_engine_from_yaml(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "dummy.txt").write_text("ok", encoding="utf-8")
    cfg = {
        "steps": [{"id": "soumettre_dossier"}],
        "data_folder": str(data_dir),
        "audit_folder": str(tmp_path / "audit"),
        "log_folder": str(tmp_path / "logs"),
    }
    yaml_file = tmp_path / "wf.yaml"
    yaml_file.write_text(yaml.dump(cfg), encoding="utf-8")
    engine = WorkflowCertifEngine.from_yaml(yaml_file, {"soumettre_dossier": SoumettreDossierStep})
    assert len(engine.steps) == 1

