import datetime
import json
import logging

import pandas as pd

utils_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/services.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s  вызов %(funcName)s из %(filename)s: %(message)s")
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)
utils_logger.setLevel(logging.DEBUG)

utils_logger.debug("Использовано функция")
utils_logger.info("Выполнено успешно")
utils_logger.warning("Предупреждение")
utils_logger.error("Имеется ошибка данных - чего не хватает")
utils_logger.critical("Все данные  неверны, входящий файл не подходит")


def profitable_cashback(file_path: str, number_mouth: str, number_year: str) -> str:
    """Функция для анализа выгодности категорий повышенного кешбэка.
    На вход функции поступают данные для анализа, год и месяц."""
    try:
        mouth_year = ["01"]
        mouth_year.append(number_mouth)
        mouth_year.append(number_year)
        mouth_year_str = "-".join(mouth_year)
        data_start = datetime.datetime.strptime(mouth_year_str, "%d-%m-%Y")
        date_end = (data_start.replace(day=28) + datetime.timedelta(days=7)).replace(day=1) - datetime.timedelta(
            days=1
        )
        df = pd.read_excel(file_path)
        df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], format="%d.%m.%Y")  # форматируем в исходном файле дату
        df = df[(df["Дата платежа"] >= data_start) & (df["Дата платежа"] <= date_end)]  # оставляем операции в периоде

        df = df.groupby("Категория")["Сумма операции с округлением"].sum()
        df_dict = df.to_dict()

        for key, value in df_dict.items():
            df_dict[key] = round(value * 0.01, 2)
        json_df_dict = json.dumps(df_dict)
        utils_logger.debug("Использовано функция")
        utils_logger.info("Выполнено успешно")
        return json_df_dict
    except Exception as e:
        utils_logger.warning("Предупреждение")
        utils_logger.error("Имеется ошибка данных - чего не хватает")
        utils_logger.critical("Все данные  неверны, входящий файл не подходит")
        raise Exception(f"Ошибка {e} столбец не найден")
