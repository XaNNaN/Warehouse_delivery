"""
Модуль функций исполняющих sql запросы в рамках курсора.
"""

from tools.db.db_conn import DBConnection


def work_with_db(dbconfig, _SQL):
    """
    Выполняет запрос и возращает список словарей, как результат запроса

    Args:
        dbconfig: json. Параметры подключения.
        _SQL: str. Строка sql запроса.

    Returns:
        result: list of dicts. Резульат sql запроса.
    """
    with DBConnection(dbconfig) as cursor:
        if cursor is None:
            raise ValueError(10001)
        elif cursor:
            cursor.execute(_SQL)

            result = []

            schema = [column[0] for column in cursor.description]

            for row in cursor.fetchall():
                result.append(dict(zip(schema, row)))

            return result


# редактирование таблицы
def make_update(db_config, sql):
    """
    Функция для редактирования таблицы. По результату не строится таблица в шаблонах.

    Args:
        db_config: json. Параметры подключения.
        sql: str. Строка sql запроса.

    Returns:
         a: int, list of dicts. Статус создания курсора или содержимое запроса.
    """
    with DBConnection(db_config) as cursor:
        a = None
        a = cursor.execute(sql)
    if a is None:
        return -2
    return a
