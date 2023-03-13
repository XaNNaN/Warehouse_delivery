"""Модуль для функций к декоратору ограничения доступа к blueprint'у."""

from functools import wraps

from flask import session, current_app, request, render_template


# Извлечение группы из сессии и нахождение её прав в конфиге
def group_permission_validation():
    """
    Функция определения прав группы пользователя через сессию.

    Returns:
         Bool. Определяет, есть ли пользователя права в этому blueprint'у.
    """
    access_config = current_app.config['ACCESS']
    group = session.get('group', 'unauthorized')

    url = request.endpoint.split('.')
    target_app = '' if len(url) == 1 else url[0]

    return group in access_config and target_app in access_config[group]


def group_permission_validation_decorator(func):
    """
    Декоратор с декорированием внутренней функции

    Args:
        func: function. Декорируемая функция.

    Returns:
        func. Возвращает функцию-обёртку.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Сама обёртка

        Args:
            *args: list, **kwargs: dict. Аргументы для передачи в функцию

        Returns:
            результат выполнения декорируемой функции или HTML строку контента.
            Если у пользователя нет прав на текущий url адрес,
            то его возврящает в главное меню.

        """
        if group_permission_validation():
            return func(*args, **kwargs)
        return render_template('result_1.html')

    return wrapper
