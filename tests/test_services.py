import json
import os
import tempfile
import unittest

import pandas as pd

from src.services import profitable_cashback


class TestProfitableCashback(unittest.TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.test_data = [
            # Данные за май 2023 (должны войти в отчет)
            ["01.05.2023", "Супермаркеты", 1000],
            ["15.05.2023", "АЗС", 500],
            ["31.05.2023", "Рестораны", 3000],
            # Данные за другие месяцы (не должны войти)
            ["30.04.2023", "Такси", 700],
            ["01.06.2023", "Аптеки", 400],
            # Несколько операций в одной категории
            ["10.05.2023", "Супермаркеты", 2000],
            ["20.05.2023", "Супермаркеты", 500],
        ]

    def create_test_file(self):
        """Создает временный Excel-файл с тестовыми данными"""
        df = pd.DataFrame(self.test_data, columns=["Дата платежа", "Категория", "Сумма операции с округлением"])

        temp_file = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
        df.to_excel(temp_file.name, index=False)
        return temp_file.name

    def test_basic_functionality(self):
        """Тест основной функциональности"""
        file_path = self.create_test_file()

        # Вызываем тестируемую функцию
        result = profitable_cashback(file_path, "05", "2023")
        os.unlink(file_path)  # Удаляем временный файл

        # Преобразуем результат
        result_dict = json.loads(result)

        # Проверяем ожидаемые результаты
        expected = {
            "Супермаркеты": 35.0,  # (1000+2000+500)*0.01
            "АЗС": 5.0,  # 500*0.01
            "Рестораны": 30.0,  # 3000*0.01
        }

        self.assertEqual(result_dict, expected)

    def test_empty_month(self):
        """Тест для месяца без данных"""
        file_path = self.create_test_file()

        # Вызываем для месяца без данных (апрель 2023)
        result = profitable_cashback(file_path, "04", "2023")
        os.unlink(file_path)

        result_dict = json.loads(result)
        self.assertEqual(result_dict, {"Такси": 7.0})
