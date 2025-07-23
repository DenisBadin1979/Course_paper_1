import datetime
from typing import Any, Optional

import pandas as pd


def my_decorator_noarg(func: Any) -> Any:
    """Декоратор без параметра — записывает данные отчета в файл с названием по умолчанию"""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        df = func(*args, **kwargs)
        df.to_excel("data/report.xlsx", index=False, sheet_name="report")

    return wrapper


def my_decorator_arg(file_record: str) -> Any:
    """Декоратор с параметром — принимает имя файла в качестве параметра."""

    def my_decorator(func: Any) -> Any:
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            result.to_excel(file_record, index=False, sheet_name="report")

        return inner

    return my_decorator


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    if date is None:
        date_end = datetime.datetime.now()
    else:
        date_end = datetime.datetime.strptime(date, "%d.%m.%Y")

    num_y = int(date_end.strftime("%Y")) - 1
    num_m = int(date_end.strftime("%m")) - 2
    if num_m <= 0:
        num_m = 12 + num_m
        date_start = date_end.replace(year=num_y, month=num_m, day=1)
    else:
        date_start = date_end.replace(month=num_m, day=1)
    df = transactions
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], format="%d.%m.%Y")  # форматируем в исходном файле дату
    df = df[(df["Дата платежа"] >= date_start) & (df["Дата платежа"] <= date_end) & (df["Категория"].isin([category]))]
    df = df.groupby("Категория")["Сумма операции с округлением"].sum()
    return df
