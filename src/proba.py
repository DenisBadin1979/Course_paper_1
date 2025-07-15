import datetime
from utils import greeting_user, reader_transaction_excel
import pandas as pd

name_path = 'data/operations.xlsx'
df = reader_transaction_excel(name_path)
# df = df.rename(columns={
#     'Дата платежа': 'date pay',
#     'Номер карты': 'nuber kart',
#     'Сумма платежа': 'total pay'
# })
date_end = datetime.datetime(2021, 3, 25,)
data_start = date_end.replace(day=1)
df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], format='%d.%m.%Y')
df = df[(df['Дата платежа'] >= data_start) & (df['Дата платежа'] <= date_end)]




print(date_end)
print(data_start)
print(df)