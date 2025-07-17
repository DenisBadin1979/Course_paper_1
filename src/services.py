import datetime
import json
import pandas as pd







def profitable_cashback (file_path: str, number_mouth: str, number_year : str ) -> str:
    """Функция для анализа выгодности категорий повышенного кешбэка.
     На вход функции поступают данные для анализа, год и месяц."""
    mouth_year = ['01']
    mouth_year.append(number_mouth)
    mouth_year.append(number_year)
    mouth_year_str = '-'.join(mouth_year)
    data_start = datetime.datetime.strptime(mouth_year_str, "%d-%m-%Y")
    date_end = (data_start.replace(day=28) + datetime.timedelta(days=7)).replace(day=1) - datetime.timedelta(days=1)
    df = pd.read_excel(file_path)
    df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], format='%d.%m.%Y') # форматируем в исходном файле дату
    df = df[(df['Дата платежа'] >= data_start) & (df['Дата платежа'] <= date_end)] # оставляем операции в периоде
    df = df.drop(['Дата операции','Номер карты', 'Статус', 'Сумма операции', 'Валюта операции', 'Валюта платежа',
                  'Кэшбэк', 'MCC', 'Бонусы (включая кэшбэк)',
                  'Округление на инвесткопилку', 'Сумма платежа', 'Дата платежа', 'Описание'], axis=1)
    df = df.groupby('Категория')['Сумма операции с округлением' ].sum()
    df_dict = df.to_dict()
    for key, value in df_dict.items():
        df_dict[key] = round(value * 0.01, 2)
    json_df_dict = json.dumps(df_dict)

    return json_df_dict


# number_mouth = '06'
# number_year = '2024'
# name_path = 'data/operations.xlsx'
#
#
# print(profitable_cashback(name_path, number_mouth, number_year ))
