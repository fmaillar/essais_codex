"""Workflow step creating a submission archive."""

from __future__ import annotations

import logging
import shutil

from ..certification_dossier import CertificationDossier
from ..workflow_engine import EtapeWorkflow

logger = logging.getLogger(__name__)


class SoumettreDossierStep(EtapeWorkflow):
    """Archive the data directory for submission."""

    id = "soumettre_dossier"

    def run(self, dossier: CertificationDossier) -> bool:
        archive = dossier.audit_path("dossier_soumission.zip")
        try:
            data_dir = dossier.data_dir
            if not data_dir.exists():
                raise FileNotFoundError(f"Dossier introuvable: {data_dir}")
            if archive.exists():
                archive.unlink()
            shutil.make_archive(archive.with_suffix(""), "zip", data_dir)
        except Exception as exc:  # pragma: no cover
            logger.exception("Erreur creation archive: %s", exc)
            return False

        logger.info("Archive generee: %s", archive)
        return True
