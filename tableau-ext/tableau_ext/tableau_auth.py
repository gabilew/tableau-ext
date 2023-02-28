"""
Tableau authentication module
"""
import os
import requests
from typing import Mapping, Any



class TableauAuth:
    """authentication class"""

    def __init__(self, config: Mapping[str, Any]):
        self.token_secret = config.get("TOKEN_SECRET", None)
        self.token_name = config.get("TOKEN_NAME", None)
        self.api_version = config.get("API_VERSION", None)
        #try:
        self.auth_url = os.path.join(
            config.get("BASE_URL"),
            self.api_version,
            "auth/signin"
        )

    def sign_in(self):
        """sign in to tableau to get the api token to make other requests
        Returns:
            requests.response: response with updated header
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

    def get_headers(self):
        """get the headers with updated api token after signing in"""
        self.sign_in()
        headers={}
        headers["X-Tableau-Auth"] = self.api_token
        headers["Accept"] = "application/json"
        return headers

