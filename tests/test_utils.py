import datetime
import unittest
from unittest.mock import patch, Mock, MagicMock
from unittest.mock import Mock
import pandas as pd
import pytest
from unittest.mock import patch
import src.utils
import requests
from src.utils import greeting_user, reader_transaction_excel, total_card, total_transaction
from src.utils import  currency_converter, stock_sandp500


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



# Тест обработки отсутствия файла
@patch('src.utils.utils_logger', new_callable=MagicMock)
def test_file_not_found(mock_logger):
    with pytest.raises(FileNotFoundError):
        reader_transaction_excel("non_existent_file.xlsx")


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'Номер карты': ['*5678', '*9012', '*1111'],
        'Сумма операции с округлением': [100.0, 200.0, 300.0],
        # Остальные колонки, которые будут удаляться
        'Дата операции': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Дата платежа': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Статус': ['OK', 'OK', 'OK'],
        'Сумма операции' : [100.0, 200.0, 300.0],
        'Валюта операции': ['RUB', 'RUB', 'RUB'],
        'Валюта платежа': ['RUB', 'RUB', 'RUB'],
        'Кэшбэк': [0.0, 0.0, 0.0],
        'Категория': ['Еда', 'Транспорт', 'Развлечения'],
        'MCC': [5678, 9012, 1111],
        'Описание': ['Покупка', 'Такси', 'Кино'],
        'Бонусы (включая кэшбэк)': [0, 0, 0],
        'Округление на инвесткопилку': [0.0, 0.0, 0.0],
        'Сумма платежа': [100, 200, 300]
    })


# Тест успешного выполнения
@patch('src.utils.utils_logger', new_callable=MagicMock)
def test_total_card_success(mock_logger, sample_df):
    # Вызываем тестируемую функцию
    result = total_card(sample_df)

    # Проверяем результат
    assert len(result) == 3
    assert result == [
        {"last_digital": "1111", "total_spent": 300.0, "cashback": 3.0},
        {"last_digital": "5678", "total_spent": 100.0, "cashback": 1.0},
        {"last_digital": "9012", "total_spent": 200.0, "cashback": 2.0}
        ]


# Тест обработки отсутствия колонки
@patch('src.utils.utils_logger', new_callable=MagicMock)
def test_total_card_missing_column(mock_logger):
    # Создаем DataFrame без нужной колонки
    df = pd.DataFrame({
        'Неправильная колонка': [1, 2, 3],
        'Другая колонка': ['a', 'b', 'c']
    })

    # Проверяем исключение
    with pytest.raises(Exception) as exc_info:
        total_card(df)

    # Проверяем сообщение об ошибке
    assert "столбец не найден" in str(exc_info.value)


# Тест группировки по карте
@patch('src.utils.utils_logger', new_callable=MagicMock)
def test_total_card_grouping(mock_logger, sample_df):
    # Добавляем дубликат карты
    new_row = pd.Series({
        'Номер карты': '*5555',
        'Сумма операции с округлением': 50.0,
        # Остальные колонки могут быть любыми
        'Дата операции': '2023-01-04',
        'Дата платежа': '2023-01-04',
        'Статус': 'OK',
        'Сумма операции': 50.0,
        'Валюта операции': 'RUB',
        'Валюта платежа': 'RUB',
        'Кэшбэк': 0.0,
        'Категория': 'Еда',
        'MCC': 5555,
        'Описание': 'Покупка',
        'Бонусы (включая кэшбэк)': 0,
        'Округление на инвесткопилку': 0.0,
        'Сумма платежа': 50
    })

    df = sample_df.copy()
    df = pd.concat([df, new_row.to_frame().T], ignore_index=True)

    # Вызываем функцию
    result = total_card(df)

    # Находим карту с двумя операциями
    card_1234 = next(item for item in result if item['last_digital'] == '5555')
    assert card_1234['total_spent'] == 50.0
    assert card_1234['cashback'] == 0.50


# Фикстура для тестовых данных



# Тест успешного выполнения
@patch('src.utils.utils_logger', new_callable=MagicMock)
def test_total_transaction_success(mock_logger, sample_df):
    # Вызываем тестируемую функцию
    result = total_transaction(sample_df.copy())

    # Проверяем результат
    assert len(result) == 3  # В тестовых данных всего 3 строки
    assert result == [
        {
            'date': '03.01.2023',
            'amount': 300.00,
            'category': 'Развлечения',
            'description': 'Кино'
        },
        {
            'date': '02.01.2023',
            'amount': 200.00,
            'category': 'Транспорт',
            'description': 'Такси'
        },
        {
            'date': '01.01.2023',
            'amount': 100.00,
            'category': 'Еда',
            'description': 'Покупка'
        }
    ]


@patch('src.utils.utils_logger', new_callable=MagicMock)
def test_total_transaction_missing_column(mock_logger, sample_df):
    # Удаляем важную колонку
    df_without_column = sample_df.drop(columns=['Сумма операции с округлением'])

    with pytest.raises(Exception) as exc_info:
        total_transaction(df_without_column)

    assert "столбец не найден" in str(exc_info.value)


# Тест на преобразование даты
@patch('src.utils.utils_logger', new_callable=MagicMock)
def test_date_formatting(mock_logger, sample_df):
    result = total_transaction(sample_df.copy())
    for item in result:
        # Проверяем формат ДД.ММ.ГГГГ
        assert len(item['date'].split('.')) == 3
        day, month, year = item['date'].split('.')
        assert len(day) == 2 and len(month) == 2 and len(year) == 4


# Тест на порядок сортировки (по убыванию суммы)
@patch('src.utils.utils_logger', new_callable=MagicMock)
def test_sorting_order(mock_logger, sample_df):
    result = total_transaction(sample_df.copy())
    amounts = [item['amount'] for item in result]
    assert amounts == sorted(amounts, reverse=True)


# Тест на количество возвращаемых элементов
@patch('src.utils.utils_logger', new_callable=MagicMock)
def test_max_5_transactions(mock_logger):
    # Создаем DF с 10 строками
    data = {
        'Сумма операции с округлением': [i * 100 for i in range(10)],
        'Дата платежа': ['2023-01-01'] * 10,
        'Категория': ['Test'] * 10,
        'Описание': ['Test'] * 10
    }
    for col in [
        'Дата операции', 'Номер карты', 'Статус', 'Сумма операции',
        'Валюта операции', 'Валюта платежа', 'Кэшбэк', 'MCC',
        'Бонусы (включая кэшбэк)', 'Округление на инвесткопилку', 'Сумма платежа'
    ]:
        data[col] = [''] * 10

    df = pd.DataFrame(data)
    result = total_transaction(df)
    assert len(result) == 5

@patch('requests.get')
def test_currency_converter(mock_get):
    mock_get.return_value.json.return_value = {'login': 'testuser', 'name': 'Test User'}
    assert currency_converter('testuser') == {'login': 'testuser', 'name': 'Test User'}



