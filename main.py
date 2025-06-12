"""Entry point for the object oriented certification workflow."""

from __future__ import annotations

import sys
from pathlib import Path

from core import WorkflowCertifEngine
from core.etapes import (
    CheckExigencesStep,
    CheckMOPStep,
    CheckPreuvesStep,
    SoumettreDossierStep,
    GererRetoursStep,
)

STEP_MAP = {
    "check_exigences": CheckExigencesStep,
    "check_mop": CheckMOPStep,
    "check_preuves": CheckPreuvesStep,
    "soumettre_dossier": SoumettreDossierStep,
    "gerer_retours": GererRetoursStep,
}


def main(yaml_path: str = "workflow_certif.yaml") -> None:
    """Run the workflow defined in ``yaml_path``."""
    engine = WorkflowCertifEngine.from_yaml(Path(yaml_path), STEP_MAP)
    rc = engine.run()
    if rc != 0:
        sys.exit(rc)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run certification workflow")
    parser.add_argument("--yaml", default="workflow_certif.yaml", help="Path to configuration YAML")
    args = parser.parse_args()
    main(args.yaml)
