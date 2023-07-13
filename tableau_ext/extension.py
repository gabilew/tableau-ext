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
CMD_REFRESH = "refresh"


class Tableau(ExtensionBase):
    """Extension implementing the ExtensionBase interface."""

    def __init__(self) -> None:
        """Initialize the extension."""
        self.tableau_bin = "tableau"
        self.env_config = {}

    def _setup_config(self) -> None:
        self.env_config = prepared_env(ENV_PREFIX)

        authenticator = TableauAuth(self.env_config)
        authenticator.sign_in()
        self.tableau_headers = authenticator.get_headers()
        self.base_url = os.path.join(
            self.env_config["BASE_URL"], self.env_config["API_VERSION"]
        )

        self.site_id = self.env_config["SITE_ID"]

    def invoke(self, command_name: str | None, *command_args: Any) -> None:
        """Invoke the underlying api, that is being wrapped by this extension.

        Args:
            command_name: The name of the command to invoke.
            command_args: The arguments to pass to the command.

        Returns None
        """
        command_name, command_args = command_args[0], command_args[1:]
        if command_name == CMD_REFRESH:
            log.info(self._refresh(command_args).text)
        else:
            log.error(f"Command {command_name} not supported")

    def _refresh(self, *args: Any) -> requests.Response:
        """Method to call refresh request.

        Args:
            datasource_id (str): datasource id to be refreshed.

        Returns:
            requests.Response: respose of the refresh request.
        """
        self._setup_config()

        if len(args[0]) > 1:
            raise Exception(f"Invalid args. Only allowed argument is the Datasoure LUID, args recieved: {len(args[0])}")

        if len(args[0]) == 1:
            datasource_id = self._get_datasource_luid(args[0][0])
        else:
            datasource_id = self._get_datasource_luid(None)

        return refresh(
            datasource_id=datasource_id,
            site_id=self.site_id,
            url=self.base_url,
            headers=self.tableau_headers,
        )

    def _get_datasource_luid(self, luid):
        if luid is None:
            id = self.env_config.get("DATASOURCE_LUID", "")
            if id == "":
                raise Exception("DATASOURCE_LUID env var not defined")
            return id

        if type(luid) != str:
            raise TypeError("luid is not of type str")

        return luid

    def describe(self) -> models.Describe:
        """Describe the extension.

        Returns:
            The extension description
        """
        return models.Describe(
            commands=[
                models.ExtensionCommand(
                    name="tableau_extension",
                    description="extension commands",
                    commands=[CMD_REFRESH]
                ),
                models.InvokerCommand(
                    name="tableau_invoker",
                    description="pass through invoker",
                    commands=[f":{CMD_REFRESH}"]
                ),
            ]
        )
