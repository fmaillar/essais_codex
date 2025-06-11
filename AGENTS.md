
# 🧠 AGENTS.md – Définition des agents intelligents Codex pour le workflow de certification

Ce fichier documente les différents agents ou assistants logiques pouvant intervenir dans l’implémentation automatisée du workflow de certification CAF, tel que défini dans `workflow_certif.yaml`.

---

## 🔹 Agent Name: CertifFlowCodex

### 🎯 Rôle
CertifFlowCodex est un assistant intelligent de développement conçu pour :
- compléter automatiquement les scripts du pipeline à partir de `workflow_certif.yaml`,
- détecter les erreurs structurelles ou fonctionnelles,
- proposer des garde-fous adaptés par étape,
- générer automatiquement la documentation et les fichiers de configuration annexes (ex. : PlantUML, README, rapports d’audit).

---

## 🔍 Capacités attendues

| Capacité | Description |
|---------|-------------|
| Lecture de YAML | Analyse de `workflow_certif.yaml`, compréhension des étapes, des scripts associés et des garde-fous |
| Génération de code | Remplissage progressif de chaque script Python pour valider les exigences, preuves, MOP |
| Logging intelligent | Génération de logs horodatés par étape, centralisation dans `/logs` |
| Autonomie réflexive | Relecture du code généré pour correction immédiate (feedback -> input) |
| UML Generator | Production de `.puml` (Activity, Sequence, Use Case) alignés avec le YAML |
| Audit et diagnostic | Création de rapports TXT/CSV dans `audit/` avec traçabilité complète des anomalies |

---

## 🛠️ Exemple de prompt pour un script Python

```python
# Codex prompt
'''
Complète ce script pour :
- ouvrir le fichier Excel dans "Preuves/"
- vérifier que toutes les lignes où Applicability == "Oui" contiennent une Preuve de test et une Preuve de conception
- générer un rapport CSV listant les lignes non conformes
- si erreurs critiques : retourne 1
'''
```

---

## 🧩 Autres agents possibles

| Nom | Rôle |
|-----|------|
| `DocSyncCodex` | Synchronise le `.yaml` avec les fichiers `.puml`, crée des vues UML automatiques |
| `AuditGenCodex` | Analyse les sorties des scripts et génère des rapports lisibles pour les CAM |
| `GEDIntegrator` | Connecte la logique du workflow à un Sharepoint ou GED entreprise |

---

## 📁 Localisation recommandée

Ce fichier doit être placé à la racine du dépôt (`certif-workflow/`) avec :
- `README.md`
- `workflow_certif.yaml`
- `Makefile`
- `scripts/`
