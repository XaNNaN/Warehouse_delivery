"""Главный файл в blueprint'e оформления поставки."""

from flask import Blueprint, render_template, request, session, current_app, redirect

from tools.db.sql_provider import SQLProvider
from tools.db.work_with_db import work_with_db, make_update

from .utils import add_to_basket, claer_basket
from auth.access import group_permission_validation_decorator


basket_app = Blueprint('basket', __name__, template_folder='templates')
provider = SQLProvider('invoice/sql')


@basket_app.route('/', methods=['GET', 'POST'])
@group_permission_validation_decorator
def list_orders():
    if request.method == 'GET':
        basket = session.get('basket', [])
        ship_date = session.get('date')
        prov_name = session.get('provider_name')

        sql = provider.get('list_orders.sql')
        items = work_with_db(current_app.config['db_config'], sql)
        if items is None:
            return render_template('con_error.html')

        return render_template('basket_list_orders.html', items=items, baskets=basket, date=ship_date, name=prov_name)
    else:
        unit_price = request.form['unit_price']
        quantity = request.form['quantity']
        id_product_info = request.form['id_product_info']

        sql = provider.get('item_orders.sql', id_product_info=id_product_info)
        items = work_with_db(current_app.config['db_config'], sql)

        added = {'unit_price': unit_price, 'quantity': quantity}
        items[0].update(added)

        if items:
            add_to_basket(items[0])
        else:
            return render_template('not_found_item.html')
        return redirect('/basket')


@basket_app.route('/clear-basket')
@group_permission_validation_decorator
def clear_basket():
    claer_basket()
    return redirect('/basket')


@basket_app.route('/buy-products')
@group_permission_validation_decorator
def buy_products():
    # создадим запись о поставке
    ship_date = session.get('date')
    ship_id_provider = session.get('provider')
    print(ship_id_provider, ship_date)

    sql = provider.get('add_delivery.sql', id_prov=ship_id_provider, del_date=ship_date)
    result = make_update(current_app.config['db_config'], sql)
    if result is None:
        return render_template('con_error.html')

    # Теперь достанем из бд ID созданной поставки
    sql = provider.get('get_delivery_id.sql', id_prov=ship_id_provider, del_date=ship_date)
    delivery_id = work_with_db(current_app.config['db_config'], sql)
    if delivery_id is None:
        return render_template('con_error.html')
    print(delivery_id)
    delivery_id = delivery_id[0]['id_del']
    print(delivery_id)

    # Занесём продукты из корзины в список заказанных продуктов
    basket = session.get('basket', [])
    for i in basket:
        id_product_info = i['id_product_info']
        quantity = i['quantity']
        preice_per_unit = i['unit_price']

        sql = provider.get('add_product_in_delivery_list.sql', id_del=delivery_id, id_product_info=id_product_info,
                           preice_per_unit=preice_per_unit, quantity=quantity)
        result = make_update(current_app.config['db_config'], sql)
        if result is None:
            return render_template('con_error.html')

    # Очистим корзину, чтобы в при оформлении следующей постваки она была пуста
    claer_basket()
    return redirect('/')


@basket_app.route('/choose-provider', methods=['GET', 'POST'])
@group_permission_validation_decorator
def choose_provider():
    if request.method == 'GET':
        sql = provider.get('get_providers.sql')
        items = work_with_db(current_app.config['db_config'], sql)
        if items is None:
            return render_template('con_error.html')
        return render_template('providers.html', items=items)

    else:
        session['provider'] = request.form['id_prov']
        session['provider_name'] = request.form['prov_name']
        return redirect('/basket/choose-date')


@basket_app.route('/choose-date', methods=['GET', 'POST'])
@group_permission_validation_decorator
def choose_date():
    if request.method == 'GET':
        prov_name = session.get('provider_name')
        return render_template('date.html', name=prov_name)

    else:
        session['date'] = request.form['date']
        return redirect('/basket')
