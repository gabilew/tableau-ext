""" 
Tableau rest api resquests
"""

from typing import Dict
import requests


def refresh(datasource_id: str, site_id:str, url:str, headers: Dict) -> requests.Response:
    """Refreshes the data source

    Args:
        datasource_id (str): id of the datasource to be refreshed
        site_id (str): site id
        url (str): base url
        headers (Dict): headers
    
    Returns the response of the api call
    """
    return requests.post(
        url = url + f"/sites/{site_id}/datasources/{datasource_id}/refresh",
        headers=headers,
        json={}
    )

