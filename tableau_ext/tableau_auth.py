"""Tableau authentication module."""
import os
from typing import Dict, Mapping

import requests
import structlog

log = structlog.get_logger()


class TableauAuth:
    """authentication class."""

    def __init__(self, config: Dict[str, str]) -> None:
        """Intialises the Tableau authentication class.

            Authentication can be done either with personalAccessTokenName
            or username.

        Args:
            config (Dict[str, Any]): config file.

        Returns: None
        """
        self.token_secret = None
        self.token_name = None
        self.username = None
        self.password = None

        if "TOKEN_NAME" in config:
            self.token_secret = config["TOKEN_SECRET"]
            self.token_name = config["TOKEN_NAME"]
        else:
            self.username = config["USERNAME"]
            self.password = config["PASSWORD"]

        self.api_version = config["API_VERSION"]
        self.auth_url = os.path.join(
            config["BASE_URL"], self.api_version, "auth/signin"
        )

    def sign_in(self) -> None:
        """Sign in to tableau to get the api token to make other requests.

        Raises:
            requests.exceptions.HTTPError: http request returned status code >= 300
            Exception: payload is not complete
        """
        if self.token_name is not None:
            body = {
                "credentials": {
                    "personalAccessTokenName": self.token_name,
                    "personalAccessTokenSecret": self.token_secret,
                    "site": {"contentUrl": "saltpayreportingco"},
                }
            }
        else:
            body = {
                "credentials": {
                    "name": self.username,
                    "password": self.password,
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
        try:
            response.raise_for_status()
            payload = response.json()
            self.api_token = payload["credentials"]["token"]
        except requests.exceptions.HTTPError:
            structlog.get_logger().exception(
                f"Failed to sign in with status code {response.status_code}"
            )
            raise
        except Exception:
            structlog.get_logger().exception("Could not get api token")
            raise

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
