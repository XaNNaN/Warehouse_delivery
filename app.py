"""
Это основное приложение.
Здесь расположено главное меню и
выход с очисткой сессии.
"""

import json

from flask import Flask, render_template, session


from query.routes import query
from auth.routes import auth
from edit.routes import edit
from invoice.routes import basket_app


app = Flask(__name__)

app.config['SECRET_KEY'] = 'aanbtkfdnaaldf'  # Для защиты. Пока не используется
app.config['db_config'] = json.load(open('configs/config.json', 'r'))
app.config['ACCESS'] = json.load(open('configs/access.json', 'r'))


app.register_blueprint(query, url_prefix='/query')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(edit, url_prefix='/edit')
app.register_blueprint(basket_app, url_prefix='/basket')


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/exit_page')
def exit_page():
    session.clear()
    return render_template('exit_page.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5050)
