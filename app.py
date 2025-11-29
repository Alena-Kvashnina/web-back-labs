from flask import Flask, url_for, render_template, request
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
import datetime
import os

app = Flask(__name__)
logger = []

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

# регистрация blueprints
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)



@app.route("/")
@app.route("/index")
def index():
    lab1_web = url_for("lab1.lab")
    lab2_web = url_for("lab2.lab22")
    lab3_web = url_for("lab3.lab33")
    lab4_web = url_for("lab4.lab44")
    lab5_web = url_for("lab5.lab55")
    lab6_web = url_for("lab6.lab66")
    lab7_web = url_for("lab7.lab77")


    return f'''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
            <hr>
        </header>
        <main>
            <ul>
                <li><a href="{lab1_web}">Первая лабораторная</a></li>
                <li><a href="{lab2_web}">Вторая лабораторная</a></li>
                <li><a href="{lab3_web}">Третья лабораторная</a></li>
                <li><a href="{lab4_web}">Четвертая лабораторная</a></li>
                <li><a href="{lab5_web}">Пятая лабораторная</a></li>
                <li><a href="{lab6_web}">Шестая лабораторная</a></li>
                <li><a href="{lab7_web}">Седьмая лабораторная</a></li>
            </ul>
        </main>
        <footer>
            <hr>
            <p>Квашнина Алёна Юрьевна, ФБИ-34, 3 курс, 2025 год</p>
        </footer>
    </body>
</html>
'''


@app.errorhandler(404)
def not_found(err):
    # лог
    global logger
    now = datetime.datetime.today()
    user_ip = request.remote_addr
    requested_url = request.url
    logger.append(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] IP: {user_ip}, URL: {requested_url}")

    # HTML
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
