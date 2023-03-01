"""Tableau rest api resquests."""

from typing import Mapping

import requests
import structlog


def refresh(
    datasource_id: str, site_id: str, url: str, headers: Mapping[str, str]
) -> requests.Response:
    """Refreshes the data source.

    Args:
        datasource_id (str): id of the datasource to be refreshed.
        site_id (str): site id.
        url (str): base url.
        headers (Dict): headers.

    Raises:
        HTTPError: http request returned status code >= 300

    Returns:
        requests.Response: the response of the api call.
    """
    resp = requests.post(
        url=url + f"/sites/{site_id}/datasources/{datasource_id}/refresh",
        headers=headers,
        json={},
    )

    if resp.status_code >= 300:
        structlog.get_logger().error("failed to refresh data source")
        raise requests.exceptions.HTTPError(resp.text)

    structlog.get_logger().info(f"succesfully refreshed datasource {datasource_id}")
    return resp
