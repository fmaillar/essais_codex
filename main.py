"""Main orchestrator for the certification workflow."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml


def load_workflow(yaml_path: Path) -> dict:
    """Load YAML configuration for the workflow."""
    with yaml_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_step(step: dict) -> int:
    """Execute a workflow step via its Python script.

    Parameters
    ----------
    step : dict
        Step configuration containing the script path and identifier.

    Returns
    -------
    int
        Return code from the executed script.
    """
    script = step.get("script")
    if not script:
        print(f"⚠️  Aucun script défini pour l'étape {step['id']}")
        return 0

    print(f"🔧 Étape : {step['id']}")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode


def main(yaml_path: str) -> None:
    """Run workflow steps sequentially."""
    config = load_workflow(Path(yaml_path))
    steps = config.get("steps", [])

    for step in steps:
        rc = run_step(step)
        if rc != 0:
            print(f"❌ Étape échouée: {step['id']}")
            sys.exit(rc)

    print("✅ Workflow terminé avec succès")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run certification workflow")
    parser.add_argument("--yaml", default="workflow_certif.yaml", help="Path to configuration YAML")
    args = parser.parse_args()
    main(args.yaml)
