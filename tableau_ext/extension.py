"""Meltano Tableau extension."""
from __future__ import annotations

import os
from typing import Any

import requests
import structlog
from meltano.edk import models
from meltano.edk.extension import ExtensionBase
from tableau_ext.tableau_auth import TableauAuth
from tableau_ext.tableau_requests import refresh
from tableau_ext.utils import prepared_env

log = structlog.get_logger()

ENV_PREFIX = "TABLEAU"


class Tableau(ExtensionBase):
    """Extension implementing the ExtensionBase interface."""

    def __init__(self) -> None:
        """Initialize the extension."""
        self.tableau_bin = "tableau"
        self.env_config = prepared_env(ENV_PREFIX)

        authenticator = TableauAuth(self.env_config)
        authenticator.sign_in()
        self.tableau_headers = authenticator.get_headers()
        self.base_url = os.path.join(
            self.env_config["BASE_URL"], self.env_config["API_VERSION"]
        )

        self.site_id = self.env_config["SITE_ID"]

    def invoke(self, command_name: str | None, *command_args: Any) -> None:
        """Invoke the underlying cli, that is being wrapped by this extension.

        Args:
            command_name: The name of the command to invoke.
            command_args: The arguments to pass to the command.

        Returns None
        """
        command_name, command_args = command_args[0], command_args[1:]
        if command_name == "refresh":
            self._refresh(datasource_id=command_args[0])

    def _refresh(self, datasource_id: str) -> requests.Response:
        """Method to call refresh request.

        Args:
            datasource_id (str): datasource id to be refreshed.

        Returns:
            requests.Response: respose of the refresh request.
        """
        return refresh(
            datasource_id=datasource_id,
            site_id=self.site_id,
            url=self.base_url,
            headers=self.tableau_headers,
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
