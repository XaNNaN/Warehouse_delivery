"""
В этом модуле описан класс для подключения к БД.
"""

from typing import Optional

import pymysql as pymysql
from pymysql import OperationalError

from tools.db import errors


class DBConnection:
    """
    Класс, отображающий подключение к БД.
    """

    def __init__(self, config: dict):
        """

        Конструктор класса DBConnection.

        Args:
            config: dict. Словарь со всеми параметрами подключения
        """
        self.config = config
        self.cursor = None
        self.conn = None

    def __enter__(self) -> Optional[pymysql.cursors.Cursor]:
        """
        Открывает соединение с БД.

        Args:

        Returns:
            .cursor: Cursor. Курсор для работы с запросами.
            None. Когда не удалось создать курсор.
        """
        try:
            self.conn = pymysql.connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            print(f'Error. Code: {err.args[0]}. Description: {err.args[1]}')
            return None
        except Exception as err:
            print('Упс... Что-то пошло не так :(')
            return None

    def __exit__(self, exc_type, exc_value, exc_trace):
        """
        Закрывает соединение с БД.

        Args:
            exc_type: Тип исключения
            exc_value: Значение исключения
            exc_trace: Откуда пришло исключение

        Returns:
            True: bool. Статус закрытия подключения.
        """
        if exc_value:
            print(errors.errors.get(exc_value.args[0]))
        if self.conn is not None and self.cursor is not None:
            self.conn.commit()
            self.conn.close()
        return True
