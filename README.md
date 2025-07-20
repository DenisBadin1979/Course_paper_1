Генерация JSON-ответов для финансового дашборда
Обзор
Модуль views.py генерирует JSON-ответы для веб-страницы, отображающей финансовые данные пользователя. Данные включают информацию по картам, транзакциям, курсам валют и котировкам акций за период с начала текущего месяца до указанной даты.

Требования
Python 3.8+

Библиотеки: requests, pandas, datetime, logging

Внешние API:

Курсы валют: Frankfurter

Котировки акций: Alpha Vantage (требуется API-ключ)

Структура проекта
text
project/
├── src/
│   ├── views.py       # Основной модуль генерации JSON
│   ├── utils.py       # Вспомогательные функции
│   ├── database.py    # Работа с данными (заглушка)
│   └── config.py      # Настройки API
├── data/
│   └── user_settings.json  # Пользовательские настройки
└── tests/             # Тесты
Формат user_settings.json
json
{
  "user_currencies": ["USD", "EUR"],
  "user_stocks": ["AAPL", "GOOGL", "MSFT"]
}
Ключевые функции в views.py
Генерация JSON-ответа
generate_main_json(datetime_str: str) -> dict

Вход: Дата в формате YYYY-MM-DD HH:MM:SS

Выход: JSON-объект со структурой:

python
{
    "greeting": str,           # Приветствие по времени суток
    "cards": list,             # Данные по картам
    "top_transactions": list,  # Топ-5 транзакций
    "exchange_rates": dict,    # Курсы валют
    "stock_prices": dict       # Котировки акций
}
Вспомогательные функции

get_greeting(time: datetime.time) -> str
Возвращает приветствие ("Доброе утро" и т.д.) на основе времени

get_cards_data(start_date: datetime, end_date: datetime) -> list
Возвращает данные по картам за период

get_top_transactions(n: int, start_date: datetime, end_date: datetime) -> list
Возвращает топ-N транзакций

fetch_currency_rates(currencies: list) -> dict
Получает курсы валют через API

fetch_stock_prices(stocks: list) -> dict
Получает котировки акций через API

Логика работы
Определение периода
Для входной даты 20.05.2020 период: 01.05.2020 - 20.05.2020

python
input_date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
start_date = input_date.replace(day=1, hour=0, minute=0, second=0)
Формирование данных

Карты:

python
{
    "last_four": "4432",        # Последние 4 цифры карты
    "total_expenses": 12500.0,  # Общая сумма расходов
    "cashback": 125.0           # Кешбэк (1% от суммы)
}
Транзакции:

python
{
    "date": "2020-05-15 14:30:00",
    "amount": 4200.0,
    "merchant": "Amazon"
}
Внешние данные

Курсы валют:

python
{
    "USD": 75.50, 
    "EUR": 89.25
}
Котировки акций:

python
{
    "AAPL": 150.75, 
    "GOOGL": 2350.50
}
Пример использования
python
# Пример вызова
from src.views import generate_main_json

response = generate_main_json("2023-10-15 14:30:00")
print(response)
Тестирование
Unit-тесты (pytest):

python
def test_greeting_morning():
    assert get_greeting(datetime.time(8, 0)) == "Доброе утро"

def test_currency_fetch():
    rates = fetch_currency_rates(["USD"])
    assert "USD" in rates
Интеграционное тестирование:

python
def test_full_json_output():
    response = generate_main_json("2023-10-15 14:30:00")
    assert "cards" in response
    assert len(response["top_transactions"]) <= 5
Настройка окружения
Создайте файл src/config.py:

python
ALPHA_VANTAGE_API_KEY = "your_api_key_here"
Установите зависимости:

bash
pip install requests pandas
Логирование
Все ошибки API и обработки данных записываются в лог:

python
import logging
logging.basicConfig(filename='app.log', level=logging.ERROR)