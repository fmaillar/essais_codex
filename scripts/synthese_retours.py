"""
Script `synthese_retours.py` – Complément à `analyse_retours.py`

Objectif :
  - Produire une synthèse des retours par exigence.
  - Permet de visualiser les commentaires regroupés et d’estimer leur importance.

Entrée :
  - Fichier Excel : `data/retours.xlsx`
    avec colonnes attendues : `Exigence`, `Commentaire`, `Criticité`

Sortie :
  - Fichier Excel : `audit/synthese_retours.xlsx` structuré par criticité.

"""

import pandas as pd
from pathlib import Path


def synthese_retours(input_path: Path, output_path: Path) -> None:
    df = pd.read_excel(input_path, engine="openpyxl")

    required_cols = {"Exigence", "Commentaire", "Criticité"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Colonnes attendues manquantes dans le fichier : {required_cols}")

    grouped = df.groupby("Exigence").agg({
        "Commentaire": lambda x: " | ".join(x),
        "Criticité": lambda x: ", ".join(x)
    }).reset_index()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Tous_Retours", index=False)
        grouped.to_excel(writer, sheet_name="Synthèse", index=False)


if __name__ == "__main__":
    synthese_retours(Path("data/retours.xlsx"), Path("audit/synthese_retours.xlsx"))
