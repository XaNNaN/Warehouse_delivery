"""
Главный модуль Авторизации.
"""

from flask import Blueprint, request, render_template, session, current_app

from auth.access import group_permission_validation_decorator
from tools.db.sql_provider import SQLProvider
from tools.db.work_with_db import work_with_db


auth = Blueprint('auth', __name__, template_folder='templates')


provider = SQLProvider('auth/sql')


@auth.route('/login', methods=['GET', 'POST'])
@group_permission_validation_decorator
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        my_login = request.form.get('login')
        my_password = request.form.get('password')

        sql = provider.get('login.sql', login=my_login, password=my_password)
        result = work_with_db(current_app.config['db_config'], sql)
        if result is None:
            return render_template('login.html', error=3)

        if len(result) < 1:
            return render_template('result.html', result=f'Вы  не авторизованы.')

        for i in current_app.config['ACCESS']:
            if result[0]['role'] == i:
                role = session['group'] = result[0]['role']
                return render_template('result.html', result=f'Вы авторизованы, как {role}.')

        return 'Группы пользователя нет в конфигурационном файле. ' \
               'Вы не можете продолжить работу, позовите администратора.'
