import datetime
import logging
import os

import pandas
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


utils_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/utils.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s  вызов %(funcName)s из %(filename)s: %(message)s")
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)
utils_logger.setLevel(logging.DEBUG)

utils_logger.debug("Использовано функция")
utils_logger.info("Выполнено успешно")
utils_logger.warning("Предупреждение")
utils_logger.error("Имеется ошибка данных - чего не хватает")
utils_logger.critical("Все данные  неверны, входящий файл не подходит")


def greeting_user() -> str:
    """Приветствие в формате Доброе утро/Добрый день/Добрый вечер/Доброй ночи в зависимости от текущего времени"""
    dict_time = {
        "Доброе утро": [6, 7, 8, 9, 10],
        "Добрый день": [11, 12, 13, 14, 15],
        "Добрый вечер": [16, 17, 18, 19, 20, 21, 22],
        "Доброй ночи": [0, 1, 2, 3, 4, 5, 23],
    }

    current_date_time = datetime.datetime.now()
    current_time = current_date_time.time()
    hour = current_time.hour
    for list_hours in dict_time:
        period_hours = dict_time[list_hours]
        if hour in period_hours:
            hello_user = list_hours
    utils_logger.info("Выполнено успешно")
    return hello_user


def reader_transaction_excel(file_path: str) -> pd.DataFrame:
    """Принимает на данные с транзакциями в формате excel и возвращает dataframe и фильтрует его по операциям
    за период с начала месяца, на который выпадает входящая дата, по входящую дату"""
    try:
        df = pd.read_excel(file_path)
        date_end = datetime.datetime.now()
        data_start = date_end.replace(day=1)
        df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], format="%d.%m.%Y")
        df = df[(df["Дата платежа"] >= data_start) & (df["Дата платежа"] <= date_end)]
        utils_logger.info("Выполнено успешно")
        return df
    except FileNotFoundError:
        utils_logger.error("Имеется ошибка данных - чего не хватает")
        raise FileNotFoundError(f"По заданному пути {file_path} ничего не найдено")


def total_card(df: pd.DataFrame) -> list[dict]:
    """Принимает dataframe из функции reader_transaction_excel и возвращает траты по каждой карте в списке словарей"""
    try:
        df = df.drop(
            [
                "Дата операции",
                "Дата платежа",
                "Статус",
                "Сумма операции",
                "Валюта операции",
                "Валюта платежа",
                "Кэшбэк",
                "Категория",
                "MCC",
                "Описание",
                "Бонусы (включая кэшбэк)",
                "Округление на инвесткопилку",
                "Сумма платежа",
            ],
            axis=1,
        )
        df = df.dropna()
        df["Номер карты"] = df["Номер карты"].str.replace("*", "", regex=False)
        df = df.groupby("Номер карты")["Сумма операции с округлением"].sum()
        df_dict = df.to_dict()
        cards_list = []
        for key, value in df_dict.items():
            card_dict = {"last_digital": key, "total_spent": round(value, 2), "cashback": round((value * 0.01), 2)}
            cards_list.append(card_dict)
        utils_logger.debug("Использовано функция")
        return cards_list

    except Exception as e:
        utils_logger.error("Имеется ошибка данных - чего не хватает")
        raise Exception(f"Ошибка {e}\n столбец не найден")


def total_transaction(df: pd.DataFrame) -> list[dict]:
    """Функция принимает DataFrame и выводит (возвращает) список словарей где указаны  ТОР5 транзакций"""
    try:
        df = df.drop(
            [
                "Дата операции",
                "Номер карты",
                "Статус",
                "Сумма операции",
                "Валюта операции",
                "Валюта платежа",
                "Кэшбэк",
                "MCC",
                "Бонусы (включая кэшбэк)",
                "Округление на инвесткопилку",
                "Сумма платежа",
            ],
            axis=1,
        )
        df = df.nlargest(5, "Сумма операции с округлением")
        df = df.reset_index(drop=True)
        df["Дата платежа"] = pd.to_datetime(df["Дата платежа"]).dt.strftime("%d.%m.%Y")
        df_list = df.to_dict(orient="records")
        transaction_list = []
        for key in df_list:
            transaction_list.append(
                {
                    "date": key["Дата платежа"],
                    "amount": key["Сумма операции с округлением"],
                    "category": key["Категория"],
                    "description": key["Описание"],
                }
            )
        utils_logger.debug("Использовано функция")
        return transaction_list

    except Exception as e:
        raise Exception(f"Ошибка {e} столбец не найден")


def currency_converter(user_currencies: list) -> list:
    """Функцию получения курса валюты по заданным в списке валют"""
    try:
        url = "https://api.apilayer.com/exchangerates_data/latest"
        str_cur = ", ".join(user_currencies)
        payload = {"base": "RUB", "symbols": str_cur}
        api_key_d = os.getenv("API_KEY_CUR")
        headers = {"apikey": api_key_d}
        response = requests.get(url, headers=headers, params=payload)
        result_convert = response.json()
        rate_currency = result_convert["rates"]
        list_currency = []
        for key, value in rate_currency.items():
            list_currency.append({"currency": key, "rate": round(1 / value, 2)})
        utils_logger.debug("Использовано функция")
        return list_currency

    except Exception as e:
        utils_logger.error("Имеется ошибка данных - чего не хватает")
        raise Exception(f"Ошибка {e}")


def stock_sandp500(stocks: list) -> list:
    """Функцию получения курса акций S&P500"""
    try:
        api_key_dt = os.getenv("API_KEY_STOCK")
        list_stock = []
        for ak in range(len(stocks)):
            response = requests.get(
                f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" f"{stocks[ak]}&apikey={api_key_dt}"
            )
            result_stock = response.json()
            stock_i = result_stock.get("Global Quote")
            dict_i = {"stock": stock_i.get("01. symbol"), "prices": stock_i.get("05. price")}
            list_stock.append(dict_i)

        utils_logger.debug("Использовано функция")
        return list_stock

    except Exception as e:
        utils_logger.error("Имеется ошибка данных - чего не хватает")
        raise Exception(f"Ошибка {e}")
