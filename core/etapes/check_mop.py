"""Workflow step validating MOP presence."""

from __future__ import annotations

import logging

from scripts.check_mop import check_mop
from ..certification_dossier import CertificationDossier
from ..workflow_engine import EtapeWorkflow

logger = logging.getLogger(__name__)


class CheckMOPStep(EtapeWorkflow):
    """Check MOP availability for each applicable requirement."""

    id = "check_mop"

    def run(self, dossier: CertificationDossier) -> bool:
        audit_file = dossier.audit_path("mop_manquants.csv")
        try:
            data_file = dossier.data_path("mop.xlsx")
            invalid_rows = check_mop(data_file)
        except Exception as exc:  # pragma: no cover
            logger.exception("Erreur MOP: %s", exc)
            return False

        if not invalid_rows.empty:
            dossier.save_csv(invalid_rows, audit_file.name)
            logger.warning("MOP manquants: %d", len(invalid_rows))
            return False
        return True
