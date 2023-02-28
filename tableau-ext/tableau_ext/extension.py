"""Meltano Tableau extension."""
from __future__ import annotations

import os
import pkgutil
import subprocess
import sys
from pathlib import Path
import requests
from typing import Any

import structlog
from meltano.edk import models
from meltano.edk.extension import ExtensionBase
from meltano.edk.process import Invoker, log_subprocess_error

from tableau_auth import TableauAuth
from utils import prepared_env

log = structlog.get_logger()

ENV_PREFIX = "TABLEAU_"

class Tableau(ExtensionBase):
    """Extension implementing the ExtensionBase interface."""

    def __init__(self) -> None:
        """Initialize the extension."""
        self.tableau_bin = "tableau"
        self.tableau_invoker = Invoker(self.tableau_bin)
        self.env_config = prepared_env(ENV_PREFIX)
        authenticator = TableauAuth(self.env_config)
        authenticator.sign_in()
        self.tableau_headers = authenticator.get_headers()

    def invoke(self, command_name: str | None, *command_args: Any) -> None:
        """Invoke the underlying cli, that is being wrapped by this extension.

        Args:
            command_name: The name of the command to invoke.
            command_args: The arguments to pass to the command.
        """
        try:
            self.tableau_invoker.run_and_log(command_name, *command_args)
        except subprocess.CalledProcessError as err:
            log_subprocess_error(
                f"tableau {command_name}", err, "Tableau invocation failed"
            )
            sys.exit(err.returncode)

    def describe(self) -> models.Describe:
        """Describe the extension.

        Returns:
            The extension description
        """
        # TODO: could we auto-generate all or portions of this from typer instead?
        return models.Describe(
            commands=[
                models.ExtensionCommand(
                    name="tableau_extension", description="extension commands"
                ),
                models.InvokerCommand(
                    name="tableau_invoker", description="pass through invoker"
                ),
            ]
        )
