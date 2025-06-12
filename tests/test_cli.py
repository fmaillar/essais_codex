"""Unit tests for the workflow orchestrator."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import run_step, run_main


def _create_script(script_path: Path, exit_code: int = 0) -> Path:
    """Create a temporary Python script that exits with ``exit_code``."""
    script_path.write_text(f"import sys\nsys.exit({exit_code})\n", encoding="utf-8")
    return script_path


def test_run_step_success(tmp_path: Path) -> None:
    """Verify ``run_step`` returns ``0`` for a successful script."""
    script = _create_script(tmp_path / "ok.py", 0)
    rc = run_step({"id": "ok", "script": str(script)})
    assert rc == 0


def test_run_step_missing_script() -> None:
    """``run_step`` should succeed when no script is provided."""
    rc = run_step({"id": "noop"})
    assert rc == 0


def test_main_success(tmp_path: Path) -> None:
    """``main`` runs every step and returns normally when all succeed."""
    script = _create_script(tmp_path / "ok.py", 0)
    config: dict[str, list[dict[str, Any]]] = {"steps": [{"id": "ok", "script": str(script)}]}
    yaml_file = tmp_path / "workflow.yaml"
    yaml_file.write_text(yaml.dump(config), encoding="utf-8")

    run_main(str(yaml_file))


def test_main_failure(tmp_path: Path) -> None:
    """``main`` exits with the failing step's return code."""
    ok_script = _create_script(tmp_path / "ok.py", 0)
    bad_script = _create_script(tmp_path / "bad.py", 1)
    config = {
        "steps": [
            {"id": "ok", "script": str(ok_script)},
            {"id": "bad", "script": str(bad_script)},
        ]
    }
    yaml_file = tmp_path / "workflow.yaml"
    yaml_file.write_text(yaml.dump(config), encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        run_main(str(yaml_file))
    assert exc.value.code == 1
