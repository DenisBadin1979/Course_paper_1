import os
import json

import requests
from dotenv import load_dotenv

load_dotenv()


def stock_sandp500(stocks:list) -> list:
    """Функцию получения курса акций S&P500"""
    api_key_dt = os.getenv("API_KEY_STOCK")
    list_stock = []
    for ak in stocks:
        response = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='
                                f'{ak}&apikey={api_key_dt}')
        result_convert = response.json()

        # list_stock.append({'stock' : ak, 'prise' : result_convert["Global Quote"]["05. price"]})


        return result_convert

di = {
    "Global Quote": {
        "01. symbol": "AMZN",
        "02. open": "281.5000",
        "03. high": "283.4566",
        "04. low": "280.9000",
        "05. price": "282.0000",
        "06. volume": "3337168",
        "07. latest trading day": "2025-07-17",
        "08. previous close": "281.9200",
        "09. change": "0.0800",
        "10. change percent": "0.0284%"
    },
    {
        "01. symbol": "AAPL",
        "02. open": "281.5000",
        "03. high": "283.4566",
        "04. low": "280.9000",
        "05. price": "1000.00",
        "06. volume": "3337168",
        "07. latest trading day": "2025-07-17",
        "08. previous close": "281.9200",
        "09. change": "0.0800",
        "10. change percent": "0.0284%"
    }
}
stocks = ["AAPL", "AMZN"]
ist_stock = []
for ak in stocks:
    result_convert = response.json()

    ist_stock.append({'stock' : ak, 'prise' : result_convert["Global Quote"]["05. price"]})

print(ist_stock)

# w = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
# print (stock_sandp500(w))

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=KIX4AAXA25W0XXH2'
r = requests.get(url)
data = r.json()

# print(data)