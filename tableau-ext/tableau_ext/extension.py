"""Meltano Tableau extension."""
from __future__ import annotations

import os
import pkgutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import structlog
from meltano.edk import models
from meltano.edk.extension import ExtensionBase

from tableau_auth import TableauAuth
from tableau_requests import refresh
from utils import MissingArgError, prepared_env

log = structlog.get_logger()

ENV_PREFIX = "TABLEAU_"

class Tableau(ExtensionBase):
    """Extension implementing the ExtensionBase interface."""

    def __init__(self) -> None:
        """Initialize the extension."""
        self.tableau_bin = "tableau"
        self.env_config = prepared_env(ENV_PREFIX)
        
        authenticator = TableauAuth(self.env_config)
        authenticator.sign_in()
        self.tableau_headers = authenticator.get_headers()
        self.base_url = f"{self.env_config.get('BASE_URL')}{self.env_config.get('API_VERSION')}/"
        self.site_id = self.env_config.get("SITE_ID")

    def invoke(self, command_name: str | None, **command_kargs: Any) -> None:
        """Invoke the underlying cli, that is being wrapped by this extension.

        Args:
            command_name: The name of the command to invoke.
            command_args: The arguments to pass to the command.
        """
        if command_name == "refresh":
            if "datasource_id"  not in command_kargs:
                raise MissingArgError("datasource_id must be in command kwargs")
            else:
                if "datasource_id" is None:
                    raise ValueError("datasource_id cannot be null")
                else:
                    self._refresh(datasource_id=command_kargs["datasource_id"])
                    # TODO add logs

    def _refresh(self, datasource_id):
        return refresh(
            datasource_id=datasource_id,
            site_id=self.site_id,
            url = self.base_url,
            headers=self.tableau_headers
        )
    
    def describe(self) -> models.Describe:
        """Describe the extension.

        Returns:
            The extension description
        """

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
