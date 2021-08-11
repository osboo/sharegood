from typing import List
import requests


class AKVConnector():
    def __init__(self, akv_url:str, tenant_id: str, client_id: str, client_secret: str) -> None:
        self.akv_url = akv_url
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.azure_ad_token = self.get_azure_ad_token()

    
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
        url = f"https://{self.akv_url}/secrets/SharegoodToken?api-version=2016-10-01"
        payload = {}
        headers = {
            'Authorization': f'Bearer {self.azure_ad_token}'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json().get("value")


    def get_allowed_users(self) -> List[int]:
        url = "https://keyvault-teamcityetl.vault.azure.net/secrets/botUsersIDs?api-version=2016-10-01"
        payload = {}
        headers = {
            'Authorization': f'Bearer {self.azure_ad_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        ids_string = response.json().get("value")
        ids = ids_string.split(";")
        return ids