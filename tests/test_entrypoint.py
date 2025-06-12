from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from main import main as run_main


def test_main_success(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "file.txt").write_text("ok", encoding="utf-8")
    cfg: dict[str, Any] = {
        "steps": [{"id": "soumettre_dossier"}],
        "data_folder": str(data_dir),
        "audit_folder": str(tmp_path / "audit"),
        "log_folder": str(tmp_path / "logs"),
    }
    yaml_file = tmp_path / "wf.yaml"
    yaml_file.write_text(yaml.dump(cfg), encoding="utf-8")

    run_main(str(yaml_file))
    assert (tmp_path / "audit" / "dossier_soumission.zip").exists()


def test_main_failure(tmp_path: Path) -> None:
    cfg = {
        "steps": [{"id": "check_mop"}],
        "data_folder": str(tmp_path / "data"),
        "audit_folder": str(tmp_path / "audit"),
        "log_folder": str(tmp_path / "logs"),
    }
    yaml_file = tmp_path / "wf.yaml"
    yaml_file.write_text(yaml.dump(cfg), encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        run_main(str(yaml_file))
    assert exc.value.code == 1
