"""Logging utilities for the certification workflow."""

from __future__ import annotations

import logging
from pathlib import Path


class LoggerCertif:
    """Simple wrapper around :mod:`logging` for workflow messages."""

    def __init__(self, log_dir: Path | None = None) -> None:
        log_dir = log_dir or Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "workflow.log"
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self._logger = logging.getLogger("workflow_certif")

    def log_info(self, message: str) -> None:
        """Log an informational ``message``."""
        self._logger.info(message)

    def log_error(self, message: str) -> None:
        """Log an error ``message``."""
        self._logger.error(message)
