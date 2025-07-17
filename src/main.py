import os


import requests
from dotenv import load_dotenv

load_dotenv()


def stock_sandp500() -> list:
    """Функцию получения курса валюты по EUR, USD, CHN"""
    url = "https://api.ipstack.com/134.201.250.155"
    payload = {"base": "RUB", "symbols" : "USD, EUR, CNY"}
    api_key_dt = os.getenv("API_KEY_STOCK")
    headers = {"apikey": api_key_dt}
    response = requests.get("https://api.ipstack.com/134.201.250.155?0b88b7e0eea6bd9f202ee2bbdd624192)")
    result_convert = response.json()

    return result_convert





