import os

import requests
from typing import List

class OxylabsProxyApiClient:
    _username: str
    _password: str
    _base_proxy_url: str

    def __init__(self):
        self._username = os.environ["OXYLABS_USERNAME"]
        self._password = os.environ["OXYLABS_PASSWORD"]
        self._base_proxy_url = os.environ["OXYLABS_BASE_URL"]

    def get_proxy_ip(self) -> str:
        return self._base_proxy_url.format(self._username, self._password)