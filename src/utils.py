import datetime
import pandas as pd


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
            greetung = list_hours
    return greetung

def reader_transaction_excel(file_path: str) -> list[dict]:
    """Принимает на данные с транзакциями в формате excel  и возвращает список словарей"""
    try:
        df = pd.read_excel(file_path)
        excel_data = df.to_dict(orient="records")
        return excel_data
    except FileNotFoundError:
        raise FileNotFoundError(f"По заданному пути {file_path} ничего не найдено")
    except Exception as e:
        raise Exception(f"Ошибка {e}")