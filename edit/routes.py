"""Модуль удаления и добавления поставщиков."""

from flask import Blueprint, request, render_template, current_app, redirect

from auth.access import group_permission_validation_decorator
from tools.db.sql_provider import SQLProvider
from tools.db.work_with_db import work_with_db, make_update


edit = Blueprint('edit', __name__, template_folder='templates')


provider = SQLProvider('edit/sql')


@edit.route('/delete_provider', methods=['GET', 'POST'])
@group_permission_validation_decorator
def delete_provider():
    if request.method == 'GET':
        sql = provider.get('show_list.sql')
        result = work_with_db(current_app.config['db_config'], sql)
        if result is None:
            return render_template('con_error.html')
        heads = ['Имя', 'Город', 'Телефон', 'Дата заключения контракта', "ID контракта"]
        return render_template('delete_items.html', items=result, heads=heads)

    if request.method == 'POST':
        id_prov = request.form.get('id_prov', None)
        sql = provider.get('delete_item.sql', id_prov=id_prov)
        print(sql)
        error = make_update(current_app.config['db_config'], sql)
        print(error)

        sql = provider.get('show_list.sql')
        result = work_with_db(current_app.config['db_config'], sql)
        heads = ['Имя', 'Город', 'Телефон', 'Дата заключения контракта', "ID контракта"]
        return render_template('delete_items.html', items=result, heads=heads, error=error)


@edit.route('/add_provider', methods=['GET', 'POST'])
@group_permission_validation_decorator
def add_provider():
    if request.method == 'GET':
        return render_template('add_item.html')

    if request.method == 'POST':
        name = request.form.get('name', None)
        city = request.form.get('city', None)
        telephone = request.form.get('telephone', None)
        conclusion_date = request.form.get('conclusion_date', None)
        contract_id = request.form.get('contract_id', None)

        sql = provider.get('insert_item.sql', name=name, city=city, telephone=telephone,
                           conclusion_date=conclusion_date, contract_id=contract_id)
        print(sql)
        result = make_update(current_app.config['db_config'], sql)
        print(result)
        if result == -2:
            return render_template('add_item.html', error=result)
        return redirect('/edit/delete_provider')
