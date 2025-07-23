from typing import Any

import pandas as pd


from src.reports import spending_by_category
from src.services import profitable_cashback
from src.utils import greeting_user, reader_transaction_excel


def main() -> Any:
    print(greeting_user())
    file_operations = input('Укажите путь к файлу с операциями:      ')
    print('Введите входящую дату для анализа:')
    day_user = input('Укажите день:  ')
    mouth_user = input('Укажите месяц:  ')
    year_user = input('Укажите год:  ')
    date_list = []
    date_list.append(day_user)
    date_list.append(mouth_user)
    date_list.append(year_user)
    date_views = ".".join(date_list)
    reader_transaction_excel (file_operations, date_views)

    print("Анализ какие категории были наиболее выгодными для выбора в качестве категорий повышенного кешбэка")
    number_mouth = input('Введите месяц:  ')
    number_year = input('Введите год: ')
    profitable_cashback(file_operations, number_mouth, number_year)

    print('Отчет трат по заданной категории за последние три месяца (от переданной даты).')
    df_use = pd.read_excel(file_operations)
    for_chose = df_use['Категория'].unique()
    print(for_chose)
    for i_ch in range(len(for_chose)):
        print(f'Номер {i_ch} - Категория {for_chose[i_ch]}')
    number_user = int(input('Введите номер категории:   '))
    category_user = for_chose[number_user]
    date_user = input('Введите входящую дату для анализа:  ')
    if len(date_user) != 10:
        date_2 = None
    else:
        date_2 = date_user
    trat_categor = spending_by_category(df_use, category_user, date_2)
    return json_data, trat_categor
