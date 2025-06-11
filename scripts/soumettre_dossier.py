"""Assemble deliverables for submission."""

from __future__ import annotations

import logging
import shutil
import sys
from pathlib import Path

LOG_FILE = Path("logs/soumettre_dossier.log")
OUTPUT_ARCHIVE = Path("audit/dossier_soumission.zip")
DATA_DIR = Path("data")


def setup_logger() -> None:
    """Configure file-based logging.

    Returns
    -------
    None
        The logger is configured for this module.
    """
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def main() -> None:
    """Create an archive of the data directory.

    Returns
    -------
    None
        Exits with ``0`` on success, ``1`` if an error occurred.
    """
    setup_logger()

    if not DATA_DIR.exists():
        logging.error("Dossier %s introuvable", DATA_DIR)
        sys.exit(1)

    try:
        OUTPUT_ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
        if OUTPUT_ARCHIVE.exists():
            OUTPUT_ARCHIVE.unlink()
        shutil.make_archive(OUTPUT_ARCHIVE.with_suffix(""), "zip", DATA_DIR)
    except Exception as exc:
        logging.exception("Erreur lors de la creation de l'archive: %s", exc)
        sys.exit(1)

    logging.info("Archive de soumission creee: %s", OUTPUT_ARCHIVE)
    sys.exit(0)


if __name__ == "__main__":
    main()
