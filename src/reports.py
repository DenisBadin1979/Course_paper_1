from datetime import datetime
from typing import Optional

import pandas as pd


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    if date == None:
        date_end = datetime.datetime.now()
    else:
        date_end = datetime.datetime.strptime(date, "%d.%m.%Y")

    num_y = int(date_end.strftime('%Y')) - 1
    num_m = int(date_end.strftime('%m')) - 2
    if num_m<=0:
        num_m = 12 + num_m
        date_start = date_end.replace(year=num_y, month=num_m, day=1)
    else:
        date_start = date_end.replace(month=num_m, day=1)

    df = transactions
    df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], format='%d.%m.%Y')  # форматируем в исходном файле дату
    df = df[(df['Дата платежа'] >= date_start) & (df['Дата платежа'] <= date_end)]  # оставляем операции в периоде
    df = df.drop(['Дата операции', 'Номер карты', 'Статус', 'Сумма операции', 'Валюта операции', 'Валюта платежа',
                  'Кэшбэк', 'MCC', 'Бонусы (включая кэшбэк)',
                  'Округление на инвесткопилку', 'Сумма платежа', 'Дата платежа', 'Описание'], axis=1)
    return df

trans =  pd.read_excel('data/operations.xlsx')
print(spending_by_category(trans, "Госуслуги", "25.06.2025"))