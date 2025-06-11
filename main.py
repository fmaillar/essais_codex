"""
main.py – Orchestrateur du workflow de certification
Lit le fichier YAML, exécute les étapes et gère les erreurs, validations et logs.
"""

import yaml
import subprocess
import sys
from pathlib import Path

def load_workflow(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_step(step):
    print(f"🔧 Étape : {step['id']}")
    if 'script' in step:
        result = subprocess.run(["python", step['script']], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ Erreur dans {step['script']}")
            if step.get('on_error', 'stop') == 'stop':
                sys.exit(1)
            elif step['on_error'] == 'warn':
                print("⚠️  Avertissement : erreur ignorée")
            else:
                print("➡️  Continuation malgré l'erreur")
    else:
        print("⚠️  Aucun script défini pour cette étape")

    if step.get('requires_validation', False):
        input("⏸️  Validation requise. Appuyez sur Entrée pour continuer...")

def main(yaml_path, phase=None):
    workflow_data = load_workflow(yaml_path)
    metadata = workflow_data.get('metadata', {})
    print(f"📋 Workflow de certification – Projet : {metadata.get('projet', 'N/A')} – Version : {metadata.get('version_sti', 'N/A')}")

    for step in workflow_data['workflow']:
        if phase and step['id'] != phase:
            continue
        run_step(step)
        if phase:
            break

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--yaml", required=True, help="Chemin du fichier workflow YAML")
    parser.add_argument("--phase", help="Nom d'une étape à exécuter uniquement")
    args = parser.parse_args()
    main(args.yaml, args.phase)
