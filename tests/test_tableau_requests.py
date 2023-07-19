from unittest import TestCase, mock

from tableau_ext.tableau_requests import refresh


class TestTableauRequests(TestCase):
    def test_refresh(self) -> None:
        with mock.patch("tableau_ext.tableau_requests.requests.post") as mocked_post:
            mocked_post.return_value.status_code = 203
            resp = refresh("123", "321", "base_url", {})

            assert resp.status_code == 203
            mocked_post.assert_called_with(
                url="base_url/sites/321/datasources/123/refresh", headers={}, json={}
            )

    def test_refresh_exception_on_500(self) -> None:
        with mock.patch("tableau_ext.tableau_requests.requests.post") as mocked_post:
            mocked_post.return_value.status_code = 500

            with self.assertRaises(Exception):
                resp = refresh("123", "321", "base_url", {})
