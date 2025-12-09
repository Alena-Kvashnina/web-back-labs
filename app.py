from flask import Flask, url_for, render_template, request
import datetime
import os

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7

from models1 import db
from hr_app import hr
from config1 import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

logger = []

# РЕГИСТРАЦИЯ BLUEPRINTS
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(hr, url_prefix="/hr")


@app.route("/")
@app.route("/index")
def index():
    return f'''
    <h1>НГТУ, ФБ, WEB-программирование</h1>
    <ul>
        <li><a href="{url_for('hr.index')}">HR-сайт — карточки сотрудников</a></li>
        <li><a href="{url_for('lab1.lab')}">Лабораторная 1</a></li>
        <li><a href="{url_for('lab2.lab22')}">Лабораторная 2</a></li>
        <li><a href="{url_for('lab3.lab33')}">Лабораторная 3</a></li>
        <li><a href="{url_for('lab4.lab44')}">Лабораторная 4</a></li>
        <li><a href="{url_for('lab5.lab55')}">Лабораторная 5</a></li>
        <li><a href="{url_for('lab6.lab66')}">Лабораторная 6</a></li>
        <li><a href="{url_for('lab7.lab77')}">Лабораторная 7</a></li>
    </ul>
    <footer>
        <p>Квашнина Алёна Юрьевна, ФБИ-34, 2025</p>
    </footer>
    '''

# ОБРАБОТЧИКИ ОШИБОК
@app.errorhandler(404)
def not_found(err):
    global logger
    now = datetime.datetime.today()
    user_ip = request.remote_addr
    requested_url = request.url
    logger.append(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] IP: {user_ip}, URL: {requested_url}")

    logs_html = "".join(f"<li>{entry}</li>" for entry in logger)
    home_url = url_for("index")

    return f'''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Ошибка 404</title>
</head>
<body style="text-align:center;">
    <h1 style="font-size:120px;color:red;">404</h1>
    <h2>Страница не найдена 😢</h2>
    <p>IP: {user_ip}</p>
    <p>Время: {now.strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><a href="{home_url}">Вернуться на главную</a></p>

    <h3>Журнал 404:</h3>
    <ul>
        {logs_html}
    </ul>
</body>
</html>
''', 404


@app.errorhandler(500)
def internal_error(err):
    return '''
    <h1>500</h1>
    <h2>Внутренняя ошибка сервера</h2>
    ''', 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
