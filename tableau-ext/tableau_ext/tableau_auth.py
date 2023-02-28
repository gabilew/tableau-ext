
import requests
from typing import Mapping, Any

URL = "https://dub01.online.tableau.com/api/3.18/auth/signin"

class TableauAuth:
    """authentication class"""

    def __init__(self, config: Mapping[str, Any]):
        self.token_secret = config.get("token_secret", None)
        self.token_name = config.get("token_name", None)
        self.auth_url = URL
   
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

    def get_headers(self, r):
        self.sign_in()
        r.headers["X-Tableau-Auth"] = self.api_token
        r.headers["Accept"] = "application/json"
        return r