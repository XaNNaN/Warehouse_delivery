"""Основной файл blueprint'а работы с запросами."""

from flask import Blueprint, render_template, request, current_app

from tools.db.sql_provider import SQLProvider
from tools.db.work_with_db import work_with_db
from auth.access import group_permission_validation_decorator

provider = SQLProvider('query/sql')

query = Blueprint('query', __name__, template_folder='templates')


@query.route('work_with_query')
@group_permission_validation_decorator
def work_with_query_page():
    return render_template('work_with_query.html')


@query.route('conc_date', methods=['POST', 'GET'])
@group_permission_validation_decorator
def conc_date():
    if request.method == 'GET':
        return render_template('tab_conc_date.html')

    month = request.form.get('month', None)
    year = request.form.get('year', None)

    sql = provider.get('conc_date.sql', month=month, year=year)
    result = work_with_db(current_app.config['db_config'], sql)

    if result is None:
        return render_template('tab_conc_date.html', error=3)

    if len(result) > 0:
        line = ['ID поставщика', 'имя', 'город', "телефон", "дата заключения договора", "ID контракта"]
        return render_template('tab_conc_date.html', result=result, first_line=line, Method='POST')

    return render_template('tab_conc_date.html', error=2)


@query.route('prefix', methods=['POST', 'GET'])
@group_permission_validation_decorator
def prefix():
    if request.method == 'GET':
        return render_template('tab_prefix.html')

    _prefix = request.form.get('prefix', None)

    sql = provider.get('prefix.sql', prefix=_prefix)
    result = work_with_db(current_app.config['db_config'], sql)

    if result is None:
        return render_template('tab_prefix.html', error=3)

    if len(result) > 0:
        line = ['ID поставщика', 'имя', 'город', "телефон", "дата заключения договора", "ID контракта"]
        return render_template('tab_prefix.html', result=result, first_line=line, Method='POST')

    return render_template('tab_prefix.html', error=2)


@query.route('pr_higher', methods=['POST', 'GET'])
@group_permission_validation_decorator
def pr_higher():
    if request.method == 'GET':
        return render_template('tab_pr_higher.html')

    _price = request.form.get('price', None)
    sql = provider.get('pr_higher.sql', price=_price)
    result = work_with_db(current_app.config['db_config'], sql)

    if result is None:
        return render_template('tab_pr_higher.html', error=3)

    if len(result) > 0:
        line = ["ID продукта", "ID информации о продукте", "количество", "дата фиксации", "цена за единицу"]
        return render_template('tab_pr_higher.html', result=result, first_line=line, Method='POST')

    return render_template('tab_pr_higher.html', error=2)


@query.route('pr_category', methods=['POST', 'GET'])
@group_permission_validation_decorator
def pr_category():
    if request.method == 'GET':
        return render_template('tab_product_category.html')

    _category = request.form.get('category', None)

    sql = provider.get('product_category.sql', category=_category)
    result = work_with_db(current_app.config['db_config'], sql)

    if result is None:
        return render_template('tab_product_category.html', error=3)

    if len(result) > 0:
        line = ["ID информации о продукте", "название", "категория", "материал", "единицы измерения"]
        return render_template('tab_product_category.html', result=result, first_line=line, Method='POST')

    return render_template('tab_product_category.html', error=2)


@query.route('pr_less', methods=['POST', 'GET'])
@group_permission_validation_decorator
def pr_less():
    if request.method == 'GET':
        return render_template('tab_product_less.html')

    _quantity = request.form.get('quantity', None)

    sql = provider.get('products_less.sql', quantity=_quantity)
    result = work_with_db(current_app.config['db_config'], sql)

    if result is None:
        return render_template('tab_product_less.html', error=3)

    if len(result) > 0:
        line = ["ID продукта", "ID информации о продукте", "количество", "дата фиксации", "цена за единицу"]
        return render_template('tab_product_less.html', result=result, first_line=line, Method='POST')

    return render_template('tab_product_less.html', error=2)


@query.route('prov_del', methods=['POST', 'GET'])
@group_permission_validation_decorator
def prov_del():
    if request.method == 'GET':
        return render_template('tab_prov_del.html')

    name = request.form.get('name', None)

    sql = provider.get('prov_del.sql', name=name)
    result = work_with_db(current_app.config['db_config'], sql)

    if result is None:
        return render_template('tab_prov_del.html', error=3)

    if len(result) > 0:
        line = ["имя", "телефон", "ID доставки", "дата доставки"]
        return render_template('tab_prov_del.html', result=result, first_line=line, Method='POST')

    return render_template('tab_prov_del.html', error=2)
