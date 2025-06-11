import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import load_workflow


def test_load_workflow() -> None:
    cfg = load_workflow(Path("workflow_certif.yaml"))
    assert isinstance(cfg, dict)
    assert len(cfg.get("steps", [])) == 5
