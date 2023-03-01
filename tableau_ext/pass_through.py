"""Passthrough shim for Tableau extension."""
import sys

import structlog
from meltano.edk.logging import pass_through_logging_config
from tableau_ext.extension import Tableau


def pass_through_cli() -> None:
    """Pass through CLI entry point."""
    pass_through_logging_config()
    ext = Tableau()
    ext.pass_through_invoker(
        structlog.getLogger("tableau_invoker"),
        *sys.argv[1:] if len(sys.argv) > 1 else []
    )
