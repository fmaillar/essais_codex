"""Workflow step validating design and test evidence."""

from __future__ import annotations

import logging

from scripts.check_preuves import check_preuves, exigences_sans_preuves
from ..certification_dossier import CertificationDossier
from ..workflow_engine import EtapeWorkflow

logger = logging.getLogger(__name__)


class CheckPreuvesStep(EtapeWorkflow):
    """Verify evidence files for each applicable requirement."""

    id = "check_preuves"

    def run(self, dossier: CertificationDossier) -> bool:
        audit_prev = dossier.audit_path("preuves_manquantes.csv")
        audit_exig = dossier.audit_path("exigences_sans_preuves.csv")
        try:
            prev_file = dossier.data_path("preuves.xlsx")
            exig_file = dossier.data_path("exigences.xlsx")
            invalid_rows = check_preuves(prev_file)
            missing_exig = exigences_sans_preuves(exig_file, prev_file)
        except Exception as exc:  # pragma: no cover
            logger.exception("Erreur verification preuves: %s", exc)
            return False

        ok = True
        if not invalid_rows.empty:
            dossier.save_csv(invalid_rows, audit_prev.name)
            logger.warning("Preuves manquantes: %d", len(invalid_rows))
            ok = False
        if not missing_exig.empty:
            dossier.save_csv(missing_exig, audit_exig.name)
            logger.warning("Exigences sans preuves: %d", len(missing_exig))
            ok = False
        return ok
