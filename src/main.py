from json.decoder import NaN

from numpy import nan

from utils import greeting_user, reader_transaction_excel



dict_from_excel = (reader_transaction_excel('data/operations.xlsx'))
list_number_kart = []
for ikart in dict_from_excel:
    unic_kart  = ikart.get("Номер карты")
    if unic_kart not in list_number_kart and type(unic_kart) != float:
        list_number_kart.append(unic_kart)
    for i_num_kart in list_number_kart:
        total_kart = 0
        if unic_kart == i_num_kart:
            total_kart == int (ikart.get("Сумма платежа"))
            total_kart +=total_kart
        print(total_kart)