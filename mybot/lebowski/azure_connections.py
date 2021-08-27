import os
from typing import List
import requests


class AKVConnector():
    def __init__(self, tenant_id: str, client_id: str, client_secret: str, env="prod") -> None:
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.env = env

    def get_azure_ad_token(self) -> str:
        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"

        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'https://vault.azure.net/.default'}
        files = []
        headers = {}

        response = requests.request(
            "POST", url, headers=headers, data=payload, files=files)

        return response.json().get("access_token")

    def get_bot_token(self) -> str:
        token = self._request_from_akv("SharegoodToken")
        return token

    def get_allowed_users(self) -> List[int]:
        ids_string = self._request_from_akv("botUsersIDs")
        ids = ids_string.split(";")
        return ids

    def get_storage_connection_string(self) -> str:
        return self._request_from_akv("StorageAccountConnectionString")

    def get_gas_quotes_api_token(self) -> str:
        return self._request_from_akv("GAS_QUOTES_API_KEY")

    def get_fx_quotes_api_token(self) -> str:
        return self._request_from_akv("FX_QUOTES_API_KEY") 

    def _request_from_akv(self, secret_name: str) -> str:
        if self.env == "prod":
            url = f"https://keyvault-teamcityetl.vault.azure.net/secrets/{secret_name}?api-version=2016-10-01"
            payload = {}
            headers = {
                'Authorization': f'Bearer {self.get_azure_ad_token()}'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            result = response.json().get("value")
        else:
            result = os.getenv(f'{secret_name}')
            if result is None:
                raise ValueError(f"{secret_name} environment variable is not set")
        return result
