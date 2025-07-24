import json

from utils import (
    currency_converter,
    greeting_user,
    reader_transaction_excel,
    stock_sandp500,
    total_card,
    total_transaction,
)


def main_page(path_file_data: str, incoming_date: str) -> str:
    """Функция предоставляет JSON-ответ с данными о расходах за месяц, сумме кешбэка"""
    # Вначале приветствие пользователя в соответствии временем суток
    greetings_time = greeting_user()
    # Формируем дата фрейм с сортировкой по дате месяца
    df_user = reader_transaction_excel(path_file_data, incoming_date)
    # траты по каждой карте
    trat = total_card(df_user)
    # список словарей где указаны ТОР5 транзакций
    trans = total_transaction(df_user)
    user_currencies = currency_converter(["USD", "EUR"])
    user_stocks = stock_sandp500(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])

    dict_end = {
        "greeting": greetings_time,
        "cards": trat,
        "top_transactions": trans,
        "currency_rates": user_currencies,
        "stock_prices": user_stocks,
    }
    json_data = json.dumps(dict_end)
    return json_data
