"""Workflow step processing evaluator feedback."""

from __future__ import annotations

import logging

from scripts.gerer_retours import extract_critiques, update_traitement
from ..certification_dossier import CertificationDossier
from ..workflow_engine import EtapeWorkflow

logger = logging.getLogger(__name__)


class GererRetoursStep(EtapeWorkflow):
    """Integrate evaluator feedback and produce audit files."""

    id = "gerer_retours"

    def run(self, dossier: CertificationDossier) -> bool:
        audit_critiques = dossier.audit_path("retours_critiques.csv")
        audit_summary = dossier.audit_path("retours_traite_nontraite.csv")
        try:
            data_file = dossier.data_path("retours.xlsx")
            critiques = extract_critiques(data_file)
            summary = update_traitement(data_file)
        except Exception as exc:  # pragma: no cover
            logger.exception("Erreur gestion retours: %s", exc)
            return False

        dossier.save_csv(summary, audit_summary.name)
        if not critiques.empty:
            dossier.save_csv(critiques, audit_critiques.name)
            logger.warning("Retours critiques identifies: %d", len(critiques))
            return False
        return True
