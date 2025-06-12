# Workflow Certification CAF

This project automates document certification steps defined in `workflow_certif.yaml`.
The code exposes an object-oriented engine located in `workflow_certif/`.
Each YAML step is mapped to a class deriving from `EtapeWorkflow`.

## Requirements
- Python 3.10+
- `pandas`, `openpyxl`, `pyyaml`

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Execute the full workflow:
```bash
make run
```
The object-oriented API can be used as follows:
```python
from pathlib import Path
from workflow_certif import CertificationDossier, WorkflowCertifEngine

dossier = CertificationDossier("CAF001", Path("data"))
engine = WorkflowCertifEngine()
engine.charger_workflow(Path("workflow_certif.yaml"))
engine.lancer(dossier)
```
Run code quality checks:
```bash
make lint
```
Run tests:
```bash
make test
```
Generate HTML documentation:
```bash
make doc
```

## Repository layout
- `scripts/` individual step scripts
- `workflow_certif.yaml` workflow configuration
- `logs/` execution logs
- `audit/` CSV audit reports
- `data/` input files

## UML of the Workflow

Object-oriented class diagram for the certification pipeline:

```plantuml
@startuml
!include ./classes_workflow_certif.puml
@enduml
```

> To view this diagram, use [PlantUML](https://plantuml.com/), [VSCode + PlantUML extension](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml), or [Kroki](https://kroki.io).

