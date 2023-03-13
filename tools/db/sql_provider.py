"""
В данном модуле описан класс
для формирования sql запроса подставлением аргументов.
"""

import os
from string import Template


class SQLProvider:
    """
    Класс для подставления аргументов в sql.
    """

    def __init__(self, file_path):
        """
        Конструктор. Задаёт путь откуда считываются sql файлы и запаменает их содержимое.

        Args:
            file_path: str. Путь к sql файлам.

        """

        self._scripts = {}

        for file in os.listdir(file_path):
            _, expression = os.path.splitext(file)
            if expression == '.sql':
                self._scripts[file] = Template(open(f'{file_path}/{file}', 'r').read())

    def get(self, file_name, **kwargs):
        """
        Вставляет аргументы в sql файл.

        Args:
            file_name: str. Название файла.
            **kwargs: dict. Аргументы для вставки в sql запрос.

        Returns:
            ._scripts[file_name]: str. Строка со вставленными аргументами
        """
        return self._scripts[file_name].substitute(**kwargs)