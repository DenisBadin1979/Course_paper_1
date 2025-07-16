import datetime

import pandas
import pandas as pd


def greeting_user() -> str:
    """Приветствие в формате Доброе утро/Добрый день/Добрый вечер/Доброй ночи в зависимости от текущего времени"""
    dict_time = {
        "Доброе утро": [6, 7, 8, 9, 10],
        "Добрый день": [11, 12, 13, 14, 15],
        "Добрый вечер": [16, 17, 18, 19, 20, 21, 22],
        "Доброй ночи": [0, 1, 2, 3, 4, 5, 23]
    }

    current_date_time = datetime.datetime.now()
    current_time = current_date_time.time()
    hour = current_time.hour
    for list_hours in dict_time:
        period_hours = dict_time[list_hours]
        if hour in period_hours:
            hello_user = list_hours
    return hello_user

def reader_transaction_excel(file_path: str) -> list[dict]:
    """Принимает на данные с транзакциями в формате excel и возвращает dataframe и фильтрует его по операциям
    за период с начала месяца, на который выпадает входящая дата, по входящую дату"""
    try:
        df = pd.read_excel(file_path)
        date_end = datetime.datetime.now()
        data_start = date_end.replace(day=1)
        df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], format='%d.%m.%Y')
        df = df[(df['Дата платежа'] >= data_start) & (df['Дата платежа'] <= date_end)]
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"По заданному пути {file_path} ничего не найдено")
    except Exception as e:
        raise Exception(f"Ошибка {e}")

def total_card (df: pandas) -> list[dict]:
    """Принимает dataframe из функции reader_transaction_excel и возвращает траты по каждой карте в списке словарей"""
    try:
        df = df.drop(['Дата операции', 'Дата платежа', 'Статус', 'Сумма операции', 'Валюта операции', 'Валюта платежа',
                      'Кэшбэк', 'Категория', 'MCC', 'Описание', 'Бонусы (включая кэшбэк)',
                      'Округление на инвесткопилку', 'Сумма платежа'], axis=1)
        df = df.dropna()
        df['Номер карты'] = df['Номер карты'].str.replace('*', '', regex=False)
        df = df.groupby('Номер карты')['Сумма операции с округлением'].sum()
        df_dict = df.to_dict()
        cards_list = []
        for key, value in df_dict.items():
            card_dict = {"last_digital": key, "total_spent": round(value, 2),
                         "cashback": round((value * 0.01), 2)}
            cards_list.append(card_dict)
        return cards_list
    except Exception as e:
        raise Exception(f"Ошибка {e} столбец не найден")

def total_transaction(df: pandas) -> list[dict]:
    try:
        df = df.drop(['Дата операции', 'Номер карты', 'Статус', 'Сумма операции', 'Валюта операции', 'Валюта платежа',
                      'Кэшбэк', 'MCC', 'Бонусы (включая кэшбэк)',
                      'Округление на инвесткопилку', 'Сумма платежа'], axis=1)
        df = df.nlargest(5, 'Сумма операции с округлением')
        df = df.reset_index(drop=True)
        df['Дата платежа'] = pd.to_datetime(df['Дата платежа']).dt.strftime('%d.%m.%Y')
        df_list = df.to_dict(orient='records')
        transaction_list = []
        for key in df_list:
            transaction_list.append({'date': key['Дата платежа'], 'amount': key['Сумма операции с округлением'],
                                     'category': key['Категория'], 'description': key['Описание']})
        return transaction_list
    except Exception as e:
        raise Exception(f"Ошибка {e} столбец не найден")



name_path = 'data/operations.xlsx'
dt_period = reader_transaction_excel(name_path)
trat = total_card(dt_period)
tran = total_transaction(dt_period)
print(greeting_user())
print(trat)
print(tran)