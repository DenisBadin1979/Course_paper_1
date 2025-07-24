import json
import unittest
from unittest.mock import MagicMock, patch

# Импортируем тестируемую функцию
from src.views import main_page


class TestMainPage(unittest.TestCase):

    @patch("src.views.stock_sandp500")
    @patch("src.views.currency_converter")
    @patch("src.views.total_transaction")
    @patch("src.views.total_card")
    @patch("src.views.reader_transaction_excel")
    @patch("src.views.greeting_user")
    def test_main_page_success(
        self, mock_greeting, mock_reader, mock_total_card, mock_total_trans, mock_currency, mock_stocks
    ):
        """Тест успешного формирования JSON-ответа"""
        # 1. Подготовка мок-данных
        mock_greeting.return_value = "Добрый день"
        mock_reader.return_value = MagicMock(name="mock_dataframe")
        mock_total_card.return_value = [{"card": "Visa Gold", "total": 25430.50}]
        mock_total_trans.return_value = [
            {"id": 1, "amount": 12000, "category": "Рестораны"},
            {"id": 2, "amount": 8500, "category": "Супермаркет"},
        ]
        mock_currency.return_value = [{"currency": "USD", "rate": 0.011}, {"currency": "EUR", "rate": 0.010}]
        mock_stocks.return_value = [{"stock": "AAPL", "prices": "175.43"}, {"stock": "TSLA", "prices": "210.15"}]

        # 2. Вызов тестируемой функции
        result = main_page("user_data.xlsx", "d")

        # 3. Проверка типа результата (JSON-строка)
        self.assertIsInstance(result, str)

        # 4. Преобразование обратно в словарь для проверки структуры
        result_dict = json.loads(result)

        # 5. Проверка структуры и данных
        self.assertEqual(result_dict["greeting"], "Добрый день")
        self.assertEqual(len(result_dict["cards"]), 1)
        self.assertEqual(result_dict["cards"][0]["card"], "Visa Gold")
        self.assertEqual(len(result_dict["top_transactions"]), 2)
        self.assertEqual(result_dict["top_transactions"][1]["amount"], 8500)
        self.assertEqual(len(result_dict["currency_rates"]), 2)
        self.assertEqual(result_dict["currency_rates"][0]["currency"], "USD")
        self.assertEqual(len(result_dict["stock_prices"]), 2)
        self.assertEqual(result_dict["stock_prices"][1]["stock"], "TSLA")

        # 6. Проверка вызова зависимостей
        mock_reader.assert_called_once_with("user_data.xlsx", "d")
        mock_currency.assert_called_once_with(["USD", "EUR"])
        mock_stocks.assert_called_once_with(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])

    @patch("src.views.stock_sandp500")
    @patch("src.views.currency_converter")
    @patch("src.views.total_transaction")
    @patch("src.views.total_card")
    @patch("src.views.reader_transaction_excel")
    @patch("src.views.greeting_user")
    def test_json_serialization(
        self, mock_greeting, mock_reader, mock_total_card, mock_total_trans, mock_currency, mock_stocks
    ):
        """Тест корректной сериализации в JSON"""
        # Подготовка минимального рабочего набора данных
        mock_greeting.return_value = "Тестовое приветствие"
        mock_reader.return_value = MagicMock()
        mock_total_card.return_value = []
        mock_total_trans.return_value = []
        mock_currency.return_value = []
        mock_stocks.return_value = []

        # Вызов функции
        result = main_page("test.xlsx", "d")

        # Проверка валидности JSON
        try:
            parsed = json.loads(result)
            self.assertEqual(parsed["greeting"], "Тестовое приветствие")
        except json.JSONDecodeError:
            self.fail("Возвращен невалидный JSON")

    @patch("src.views.stock_sandp500")
    @patch("src.views.currency_converter")
    @patch("src.views.total_transaction")
    @patch("src.views.total_card")
    @patch("src.views.reader_transaction_excel")
    def test_greeting_inclusion(self, mock_reader, mock_total_card, mock_total_trans, mock_currency, mock_stocks):
        """Тест обязательного включения приветствия"""
        # Подготовка данных
        mock_reader.return_value = MagicMock()
        mock_total_card.return_value = []
        mock_total_trans.return_value = []
        mock_currency.return_value = []
        mock_stocks.return_value = []

        # Варианты приветствий
        for greeting in ["Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"]:
            with patch("src.views.greeting_user", return_value=greeting):
                result = main_page("test.xlsx", "d")
                result_dict = json.loads(result)
                self.assertEqual(result_dict["greeting"], greeting)
