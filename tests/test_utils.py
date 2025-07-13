import datetime
from unittest.mock import patch
from unittest.mock import Mock
from src.utils import greeting_user


def test_greeting_user ():
    mock_greeting = Mock(return_value='2025-07-13 13:50:06.118206')
    datetime.datetime.now() == mock_greeting
    assert greeting_user() == "Доброй ночи"


