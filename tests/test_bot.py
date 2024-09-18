from logging import Logger
from unittest.mock import patch

from bread_fast_bot import main


try:
    import requests
except ImportError:
    raise AssertionError('Модуль requests не установлен. Посмотрите в README, что нужно для этого сделать.')

try:
    import telegram
    from telegram import Bot
    from telegram.ext import Updater
except ImportError:
    raise AssertionError('Модуль telegram не установлен. Посмотрите в README, что нужно для этого сделать.')

try:
    import dotenv
except ImportError:
    raise AssertionError('Модуль dotenv не установлен. Посмотрите в README, что нужно для этого сделать.')


@patch.object(requests, 'get', side_effect=requests.exceptions.ConnectionError)
def test_exception_handling(get_mock):
    try:
        main.get_menu()
    except requests.exceptions.ConnectionError:
        raise AssertionError('Обработайте исключение от `requests.get при помощи try ... except')


@patch.object(Bot, 'send_message')
@patch.object(Updater, 'start_polling')
@patch.object(Updater, 'idle')
def test_main(idle_mock, start_polling_mock, send_message_mock):
    try:
        idle_mock.assert_not_called()
        start_polling_mock.assert_not_called()
    except AssertionError:
        raise AssertionError('Воспользуйтесь if __name__ == "__main__"')

    test_exception_handling()

    try:
        assert isinstance(main.logger, Logger)
    except AttributeError:
        raise AssertionError('Проинициализируйте логгер. Убедитесь, что он называется logger')
