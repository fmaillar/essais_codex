from pathlib import Path
import os
import sys
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)

from workflow import CertificationDossier, RapportImpact


def test_certification_dossier(tmp_path: Path) -> None:
    dossier = CertificationDossier('ID', tmp_path)
    dossier.charger_documents()
    dossier.statut = 'ok'
    dossier.sauvegarder_statut()
    assert (tmp_path / 'statut.txt').read_text(encoding='utf-8') == 'ok'

    df = pd.DataFrame({'A': [1]})
    dossier.enregistrer_impact(df)
    assert (tmp_path / 'impact.csv').exists()
