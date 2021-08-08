from typing import List
import requests


def get_azure_ad_token(tenant_id: str, client_id: str, client_secret: str) -> str:
    import requests

    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://vault.azure.net/.default'}
    files = []
    headers = {}

    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)

    return response.json().get("access_token")


def get_bot_token(azure_ad_token: str) -> str:
    url = "https://keyvault-teamcityetl.vault.azure.net/secrets/SharegoodToken?api-version=2016-10-01"
    payload = {}
    headers = {
        'Authorization': f'Bearer {azure_ad_token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json().get("value")


def get_allowed_users(azure_ad_token: str) -> List[int]:
    url = "https://keyvault-teamcityetl.vault.azure.net/secrets/botUsersIDs?api-version=2016-10-01"
    payload = {}
    headers = {
        'Authorization': f'Bearer {azure_ad_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    ids_string = response.json().get("value")
    ids = ids_string.split(";")
    return ids