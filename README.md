# Workflow Certification CAF

This project automates document certification steps defined in `workflow_certif.yaml`.
The refactored version relies on a small object-oriented engine located in
`core/`. Each workflow step is implemented as a class so that new stages can be
plugged easily.

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
- `core/` engine and step classes
- `scripts/` legacy procedural scripts
- `workflow_certif.yaml` workflow configuration
- `logs/` execution logs
- `audit/` CSV audit reports
- `data/` input files
