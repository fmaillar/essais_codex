# Workflow Certification CAF

This project automates document certification steps defined in `workflow_certif.yaml`.

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
- `scripts/` individual step scripts
- `workflow_certif.yaml` workflow configuration
- `logs/` execution logs
- `audit/` CSV audit reports
- `data/` input files
