import json
import os

import requests

from cs_ai_common.logging.internal_logger import InternalLogger
from cs_ai_common.proxy.proxy_client import ProxyApiClient
from cs_ai_common.typings.proxy import ProxyProviders

class OtomotoApiClient:
    _base_url: str
    proxy_api_client: ProxyApiClient

    def __init__(self):
        self._base_url = os.getenv("OTOMOTO_BASE_URL")
        self.proxy_api_client = ProxyApiClient(ProxyProviders.OXYLABS)

    def query_otomoto_ads(self, body: dict) -> requests.Response:
        entry = self.proxy_api_client.get_proxy_ip()
        InternalLogger.LogDebug(f"Using proxy: {entry}")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
        }
        
        return requests.post(self._base_url, data=json.dumps(body), headers=headers,
                            proxies={"http": entry, "https": entry}, timeout=30)
    
    def send_query(self, body: dict) -> dict:
        response = self.query_otomoto_ads(body)
        return response.json()

