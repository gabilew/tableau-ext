from unittest import TestCase, mock

import requests
from tableau_ext.tableau_requests import refresh


class MockResponse:
    def __init__(self, json_data, status_code, text):
        self.json_data = json_data
        self.status_code = status_code
        self.text = text

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.HTTPError()


class TestTableauRequests(TestCase):
    def test_refresh(self) -> None:
        with mock.patch("tableau_ext.tableau_requests.requests.post") as mocked_post:
            mocked_post.return_value.status_code = 203
            resp = refresh("123", "321", "base_url", {})

            assert resp.status_code == 203
            mocked_post.assert_called_with(
                url="base_url/sites/321/datasources/123/refresh", headers={}, json={}
            )
