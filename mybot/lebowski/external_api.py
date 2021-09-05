import requests


def get_gas_quotes(token: str) -> float:
    url = "https://api.collectapi.com/gasPrice/europeanCountries"
    payload={}
    headers = {
        'Authorization': f'{token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    for r in response.json()['results']:
        if r['country'] == 'Belarus':
            price = r['gasoline'].replace(',', '.')
            return float(price)
    raise ValueError('wrong response from gas prices API')


def get_eur_rate(token: str, target_ccy:str) -> float:
    url = f"http://api.exchangeratesapi.io/v1/latest?access_key={token}&symbols=USD,BYN,RUB&format=1"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()
    rate = r['rates'][target_ccy]
    return float(rate)
