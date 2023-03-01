"""Tableau authentication module."""
import os
from typing import Dict, Mapping

import requests


class TableauAuth:
    """authentication class."""

    def __init__(self, config: Dict[str, str]) -> None:
        """Intialises the Tableau authentication class.

        Args:
            config (Mapping[str, Any]): config file.

        Returns: None
        """
        self.token_secret = config["TOKEN_SECRET"]
        self.token_name = config["TOKEN_NAME"]
        self.api_version = config["API_VERSION"]
        self.auth_url = os.path.join(
            config["BASE_URL"], self.api_version, "auth/signin"
        )

    def sign_in(self) -> requests.Response:
        """Sign in to tableau to get the api token to make other requests.

        Returns:
            requests.response: response with updated header.
        """
        body = {
            "credentials": {
                "personalAccessTokenName": self.token_name,
                "personalAccessTokenSecret": self.token_secret,
                "site": {"contentUrl": "saltpayreportingco"},
            }
        }

        response = requests.post(
            self.auth_url,
            json=body,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        response.raise_for_status()
        self.api_token = response.json()["credentials"]["token"]
        return response

    def get_headers(self) -> Mapping[str, str]:
        """Get the headers with updated api token after signing in.

        Returns:
            Mapping[str, str]: headers to be used in the requests.
        """
        self.sign_in()
        headers = {}
        headers["X-Tableau-Auth"] = self.api_token
        headers["Accept"] = "application/json"
        return headers
