"""Workflow step verifying requirement applicability."""

from __future__ import annotations

import logging

from scripts.check_exigences import verify_exigences
from ..certification_dossier import CertificationDossier
from ..workflow_engine import EtapeWorkflow

logger = logging.getLogger(__name__)


class CheckExigencesStep(EtapeWorkflow):
    """Validate requirement applicability."""

    id = "check_exigences"

    def run(self, dossier: CertificationDossier) -> bool:
        audit_file = dossier.audit_path("exigences_incompletes.csv")
        try:
            data_file = dossier.data_path("exigences.xlsx")
            invalid_rows = verify_exigences(data_file)
        except Exception as exc:  # pragma: no cover - unexpected format
            logger.exception("Erreur analyse exigences: %s", exc)
            return False

        if not invalid_rows.empty:
            dossier.save_csv(invalid_rows, audit_file.name)
            logger.warning("Exigences non conformes: %d", len(invalid_rows))
            return False
        return True
