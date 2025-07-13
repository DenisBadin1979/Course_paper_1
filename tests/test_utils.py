import datetime
import unittest
from unittest.mock import patch, Mock, MagicMock
from unittest.mock import Mock

import src.utils
from src.utils import greeting_user, reader_transaction_excel


def test_greeting_user (return_value=None):
    mock_greeting = Mock (return_value == 2025, 7, 13, 13, 50, 6)
    datetime.datetime.now() == mock_greeting
    assert greeting_user() == "Добрый день"

@patch('src.utils.datetime.datetime')
def test_greeting_user_2 (mock_greeting_2):
    mock_greeting_2.now.return_value.time.return_value.hour = 1
    assert greeting_user() == "Доброй ночи"

class TestReaderTransactionExcel(unittest.TestCase):
    @patch("pandas.read_excel")
    def test_success_read(self, mock_read_excel):
        """Тест успешного чтения Excel-файла"""
        # Создаем мок DataFrame
        mock_df = MagicMock()
        mock_df.to_dict.return_value = {"id": {0: 1, 1: 2}, "amount": {0: 100.50, 1: 200.75}}

        # Настраиваем мок pandas.read_excel
        mock_read_excel.return_value = mock_df

        # Вызываем тестируемую функцию
        result = reader_transaction_excel("dummy.xlsx")

        # Проверяем результат
        expected = [{{'id': {0: 1, 1: 2}, 'amount': {0: 100.50, 1: 200.75}}]
        self.assertEqual(result, expected)
        mock_read_excel.assert_called_once_with("dummy.xlsx")

    @patch("pandas.read_excel")
    def test_file_not_found(self, mock_read_excel):
        """Тест обработки отсутствующего файла"""
        # Настраиваем исключение
        mock_read_excel.side_effect = FileNotFoundError("File not found")

        # Проверяем, что исключение пробрасывается правильно
        with self.assertRaises(FileNotFoundError) as context:
            reader_transaction_excel("missing.xlsx")

        self.assertIn("По заданному пути missing.xlsx ничего не найдено", str(context.exception))

    @patch("pandas.read_excel")
    def test_general_exception(self, mock_read_excel):
        """Тест обработки общего исключения"""
        # Настраиваем исключение
        mock_read_excel.side_effect = Exception("Test error")

        # Проверяем обработку исключения
        with self.assertRaises(Exception) as context:
            reader_transaction_excel("broken.xlsx")
        self.assertIn("Ошибка Test error", str(context.exception))