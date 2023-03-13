"""
Файл в blueprinte офоромления поставки
для добавления товара в корзину, очистки корзины.
"""

from flask import session


def add_to_basket(item: dict) -> None:
    """
     Функция добавления товара в корзину.

     Args:
        item: dict. Словарь отображающий товар, который необходимо добавить.
    """
    basket = session.get('basket', [])
    basket.append(item)
    session['basket'] = basket


def claer_basket() -> None:
    """Функция очистки корзины."""
    if 'basket' in session:
        session.pop('basket')
