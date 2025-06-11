
# 🛠️ Workflow de Certification Industrialisé

## 🎯 Objectif

Ce dépôt contient une implémentation modulaire du workflow de certification aligné sur l'instruction officielle.  
Il permet une **vérification automatique** des exigences, des preuves et des matrices, avec **garde-fous intégrés** et **points d’arrêt pour validation humaine**.

---

## 📂 Structure du dépôt

```
certif-workflow/
├── workflow_certif.yaml         # Définition complète du pipeline
├── README.md                    # Ce fichier
├── Makefile                     # Exécution par phase ou complète
├── scripts/                     # Scripts Python par étape
│   ├── check_exigences.py
│   ├── check_mop.py
│   ├── check_preuves.py
│   ├── gen_matrice_finale.py
│   └── analyse_retours.py
├── pivot/                       # Exigences pivot CSV ou Excel
├── Preuves/                     # Dossiers contenant les preuves à valider
├── matrices/                    # Matrices générées ou à soumettre
├── audit/                       # Rapports de vérification produits
└── logs/                        # Logs d'exécution
```

---

## 🔄 Logique du `workflow_certif.yaml`

Le fichier `workflow_certif.yaml` décrit un pipeline de certification en 5 étapes clés :

1. **Identification des exigences** (`CAM`)
2. **Allocation des MOP** (`TXE`)
3. **Vérification des preuves** (`XE`)
4. **Soumission aux évaluateurs** (`CAM`)
5. **Traitement des retours** (`CAM`)

Chaque étape inclut :
- un ou plusieurs `checks` automatisés,
- une option de `requires_validation`,
- une règle `on_error` (`stop`, `warn`, `continue`).

---

## ⚙️ Exécution du workflow

### ▶️ Tout exécuter d’un coup

```bash
make run
```

### ▶️ Exécuter une étape précise

```bash
make phase=verification_preuves
```

### ▶️ En Python (exécution séquentielle)

```bash
python main.py --yaml workflow_certif.yaml
```

---

## 📌 Comportement en cas d’erreur

| Type de problème détecté       | Action par défaut (modifiable via `on_error`) |
|-------------------------------|-----------------------------------------------|
| ID d’exigence manquant        | `stop`                                        |
| Applicabilité vide            | `stop`                                        |
| Preuve manquante              | `stop`                                        |
| Traçabilité vide              | `stop`                                        |
| Retard planification          | `warn`                                        |
| Retours critiques NoBo/DeBo   | `continue`                                    |

---

## 👤 Rôles et responsabilités

| Rôle | Étapes principales |
|------|--------------------|
| `CAM` | Identification, validation, soumission |
| `TXE` | Allocation des exigences |
| `XE` | Définition des MOP, fourniture des preuves |
| `Script` | Exécution des vérifications automatiques |
| `NoBo/DeBo` | Évaluation et retours externes |

---

## 📈 Traçabilité

Tous les audits, erreurs et rapports sont stockés dans :
- `logs/` : journal machine
- `audit/` : rapports Excel / TXT
- `matrices/` : versions générées soumises

---

## 🚀 Prochaines extensions

- Intégration dans un outil de gestion documentaire (Sharepoint, GED)
- Génération automatique du fichier `.yaml` depuis `.puml`
- Interface graphique légère (Streamlit ou TUI)

---
