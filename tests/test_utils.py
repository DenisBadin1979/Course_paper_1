import datetime
import unittest
from unittest.mock import patch, Mock, MagicMock
from unittest.mock import Mock
import pandas as pd

import src.utils
from src.utils import greeting_user, reader_transaction_excel

@patch('src.utils.datetime.datetime')
def test_greeting_user_2 (mock_greeting_2):
    mock_greeting_2.now.return_value.time.return_value.hour = 1
    assert greeting_user() == "Доброй ночи"


@patch('src.utils.datetime')
@patch ('pandas.read_excel')
def test_reader_transaction_excel (mock_read_excel, mock_date):
    expected = pd.DataFrame ({'Дата платежа' : ['17.04.2025']})
    mock_read_excel.return_value = pd.DataFrame({'Дата платежа' : ['21.02.2025', '30.03.2025', '17.04.2025']})
    mock_date.datetime.now.return_value = datetime.datetime(2025, 4, 18)
    expected['Дата платежа'] = pd.to_datetime(expected['Дата платежа'], format='%d.%m.%Y')
    # print(expected.values)
    # print(reader_transaction_excel('e').values)
    assert reader_transaction_excel('a').values == expected.values


