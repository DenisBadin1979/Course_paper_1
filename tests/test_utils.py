import datetime
from unittest.mock import patch, Mock
from unittest.mock import Mock

import src.utils
from src.utils import greeting_user


def test_greeting_user (return_value=None):
    mock_greeting = Mock (return_value == 2025, 7, 13, 13, 50, 6)
    datetime.datetime.now() == mock_greeting
    assert greeting_user() == "Добрый день"

@patch('src.utils.datetime.datetime')
def test_greeting_user_2 (mock_greeting_2):
    mock_greeting_2.now.return_value.time.return_value.hour = 1
    assert greeting_user() == "Доброй ночи"