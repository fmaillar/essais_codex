"""Command-line interface for the certification workflow."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

from workflow import CertificationDossier, WorkflowCertifEngine
import yaml


def load_workflow(yaml_path: Path) -> dict:
    """Return the parsed YAML configuration."""
    with yaml_path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def run_step(step: dict) -> int:
    """Execute a Python script defined in ``step``."""
    script = step.get("script")
    if not script:
        return 0
    result = subprocess.run(["python", script])
    return result.returncode


def run_pipeline(cfg: Path, dossier_id: str, dossier_path: Path) -> None:
    """Run the workflow sequentially based on ``cfg``."""
    engine = WorkflowCertifEngine()
    engine.charger_workflow(cfg)
    dossier = CertificationDossier(dossier_id, dossier_path)
    engine.lancer(dossier)


def run_objectif(
    name: str, cfg: Path, objectifs_file: Path, dossier_id: str, dossier_path: Path
) -> None:
    """Run steps adaptively to reach ``name`` objective."""
    engine = WorkflowCertifEngine()
    engine.charger_workflow(cfg)
    engine.charger_objectifs(objectifs_file)
    dossier = CertificationDossier(dossier_id, dossier_path)
    engine.atteindre_objectif(name, dossier)


def run_main(yaml_file: str) -> None:
    """Backward-compatible entry point used in tests."""
    config = load_workflow(Path(yaml_file))
    steps = config.get("steps", [])
    for step in steps:
        rc = run_step(step)
        if rc != 0:
            raise SystemExit(rc)


def main() -> None:
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Certification workflow")
    sub = parser.add_subparsers(dest="mode", required=True)

    p_pipeline = sub.add_parser("pipeline", help="Run pipeline from YAML")
    p_pipeline.add_argument("--yaml", default="workflow_certif.yaml")
    p_pipeline.add_argument("--dossier", default="CAF001")
    p_pipeline.add_argument("--chemin", default="data")

    p_obj = sub.add_parser("objectif", help="Run workflow to reach an objective")
    p_obj.add_argument("name")
    p_obj.add_argument("--yaml", default="workflow_certif.yaml")
    p_obj.add_argument("--objectifs", default="objectifs.yaml")
    p_obj.add_argument("--dossier", default="CAF001")
    p_obj.add_argument("--chemin", default="data")

    args = parser.parse_args()
    chemin = Path(args.chemin)
    if args.mode == "pipeline":
        run_pipeline(Path(args.yaml), args.dossier, chemin)
    else:
        run_objectif(args.name, Path(args.yaml), Path(args.objectifs), args.dossier, chemin)


if __name__ == "__main__":
    main()
