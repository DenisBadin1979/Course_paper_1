import os


import requests
from dotenv import load_dotenv

load_dotenv()


def stock_sandp500() -> list:
    """Функцию получения курса валюты по EUR, USD, CHN"""
    url = "http://api.ipstack.com/134.201.250.155"
    # payload = {"base": "RUB", "symbols" : "USD, EUR, CNY"}
    api_key_dt = os.getenv("API_KEY_STOCK")
    headers = {"apikey": api_key_dt}
    response = requests.get(url, headers=headers)
    result_convert = response.json()
    # rate_currency = result_convert['rates']
    # list_currency = []
    # for key, value in rate_currency.items():
    #     list_currency.append({'currency' : key, 'rate' : round(1/value, 2)})
    return result_convert





