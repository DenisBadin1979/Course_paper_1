from json.decoder import NaN
import pandas as pd

from numpy import nan

from utils import greeting_user, reader_transaction_excel

name_path = 'data/operations.xlsx'
df = reader_transaction_excel(name_path)
df = df.drop(['Дата операции', 'Дата платежа', 'Статус','Сумма операции','Валюта операции','Валюта платежа',
              'Кэшбэк', 'Категория', 'MCC', 'Описание', 'Бонусы (включая кэшбэк)', 'Округление на инвесткопилку',
              'Сумма операции с округлением'], axis=1)
df = df.dropna()
df = df.groupby('Номер карты')['Сумма платежа'].sum()
df_dict = df.to_dict()
print(df)

# dict_from_excel = (reader_transaction_excel('data/operations.xlsx'))
# list_number_kart = []
# for ikart in dict_from_excel:
#     unic_kart  = ikart.get("Номер карты")
#     if unic_kart not in list_number_kart and type(unic_kart) != float:
#         list_number_kart.append(unic_kart)
#     for i_num_kart in list_number_kart:
#         total_kart = 0
#         if unic_kart == i_num_kart:
#             total_kart == int (ikart.get("Сумма платежа"))
#             total_kart +=total_kart
#         print(total_kart)