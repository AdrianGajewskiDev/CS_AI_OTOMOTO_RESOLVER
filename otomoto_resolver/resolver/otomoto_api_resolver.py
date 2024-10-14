import os
from otomoto_resolver.clients.otomoto_api_client import OtomotoApiClient
from cs_ai_common.logging.internal_logger import InternalLogger
from otomoto_resolver.resolver.otomoto_resolver import Resolver


class OtomotoApiResolver(Resolver):
    _client: OtomotoApiClient
    def __init__(self):
        self._client = OtomotoApiClient()
        pass

    def resolve_url(self, seed_data: dict) -> str:
        self._resolved_url = os.getenv("OTOMOTO_BASE_URL")

    def get_resolved_url(self) -> str:
        return self._resolved_url
    
    def send_reconnaissance_request(self, body: dict):
        return self._client.send_query(body)

    def send(self, body: dict):
        try:
            return self._client.send_query(body)
        except Exception as e:
            InternalLogger.LogError(f"Error while sending request to otomoto api. {e}")
            return {}