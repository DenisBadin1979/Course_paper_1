import datetime


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
