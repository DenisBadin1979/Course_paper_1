import os
import shutil
import unittest
from unittest.mock import patch

import pandas as pd
import pytest

from src.reports import my_decorator_noarg, spending_by_category


class TestDecorator(unittest.TestCase):
    def setUp(self):
        """Создаем временную директорию для тестовых файлов"""
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """Удаляем временную директорию после тестов"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_file_creation(self):
        """Проверяем создание файла отчета"""

        # Декорируем тестовую функцию
        @my_decorator_noarg
        def test_function():
            return pd.DataFrame({"A": [1, 2], "B": ["x", "y"]})

        # Вызываем декорированную функцию
        test_function()

        # Проверяем существование файла
        self.assertTrue(os.path.exists("data/report.xlsx"))

    def test_file_content(self):
        """Проверяем содержимое файла отчета"""
        # Создаем тестовые данные
        expected_df = pd.DataFrame({"Product": ["Laptop", "Phone"], "Sales": [1500, 800]})

        # Декорируем функцию
        @my_decorator_noarg
        def test_function():
            return expected_df

        # Вызываем декорированную функцию
        test_function()

        # Читаем созданный файл
        result_df = pd.read_excel("data/report.xlsx")

        # Проверяем содержимое
        pd.testing.assert_frame_equal(result_df, expected_df)

    @patch("pandas.DataFrame.to_excel")
    def test_to_excel_call(self, mock_to_excel):
        """Проверяем параметры вызова to_excel"""

        @my_decorator_noarg
        def test_function():
            return pd.DataFrame({"D": [100]})

        test_function()

        # Проверяем, что метод был вызван
        mock_to_excel.assert_called_once()

        # Проверяем параметры вызова
        args, kwargs = mock_to_excel.call_args
        self.assertEqual(args[0], "data/report.xlsx")
        self.assertEqual(kwargs["index"], False)
        self.assertEqual(kwargs["sheet_name"], "report")


# Фикстура для создания тестового DataFrame
@pytest.fixture
def sample_transactions():
    data = {
        "Дата платежа": [
            "01.01.2023",
            "15.01.2023",
            "01.02.2023",
            "15.02.2023",
            "01.03.2023",
            "15.03.2023",
            "01.04.2023",
            "15.04.2023",
            "01.05.2023",
            "15.05.2023",
            "01.06.2023",
            "15.06.2023",
            "01.12.2024",
            "15.12.2024",
            "01.01.2025",
            "15.01.2025",
            "01.02.2025",
            "15.02.2025",
        ],
        "Категория": [
            "food",
            "food",
            "food",
            "food",
            "food",
            "food",
            "food",
            "food",
            "food",
            "food",
            "food",
            "food",
            "food",
            "food",
            "food",
            "food",
            "food",
            "food",
        ],
        "Сумма операции с округлением": [
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
        ],
    }
    return pd.DataFrame(data)


def test_custom_date_february(sample_transactions):
    # Ожидаемые даты: 1 декабря 2024 - 15 февраля 2025
    result = spending_by_category(sample_transactions, "food", "15.02.2025")

    # Ожидаемая сумма: 6 транзакций (01.12.2024-15.02.2025)
    expected = pd.Series([600], index=pd.Index(["food"], name="Категория"), name="Сумма операции с округлением")
    pd.testing.assert_series_equal(result, expected)


def test_no_results(sample_transactions):
    # Запрос для категории, которой нет в данных
    result = spending_by_category(sample_transactions, "books", "15.05.2025")

    # Ожидаем пустой Series с корректными именами
    expected = pd.Series(
        [], index=pd.Index([], dtype="object", name="Категория"), name="Сумма операции с округлением", dtype="int64"
    )
    pd.testing.assert_series_equal(result, expected)
