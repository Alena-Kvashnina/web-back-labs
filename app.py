from flask import Flask, url_for, redirect, render_template, request
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
import datetime
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')


app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)


@app.route("/")
@app.route("/index")
def index():
    lab1_web = url_for("lab1.lab")
    lab2_web = url_for("lab2.lab22")  # ссылка на вторую лабу
    lab3_web = url_for("lab3.lab33")
    lab4_web = url_for("lab4.lab44")
    lab5_web = url_for("lab5.lab55")
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
    return "нет такой страницы", 404 


@app.errorhandler(404)
def not_found(err):
    global logger
    now = datetime.datetime.today()
    user_ip = request.remote_addr
    requested_url = request.url
    
    # Добавляем запись в лог
    logger.append(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] IP: {user_ip}, URL: {requested_url}")
    
    # Формируем красивый HTML для лога
    logs_html = ""
    for entry in logger:
        logs_html += f"<li>{entry}</li>"

    # Ссылка на корень сайта
    home_url = url_for("index")
    
    return f'''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Ошибка 404</title>
    <style>
        body {{
            background-color: #ffe6e6;
            font-family: Arial, sans-serif;
            color: #333;
            text-align: center;
            padding: 20px;
        }}
        h1 {{
            font-size: 150px;
            color: red;
            text-shadow: 2px 2px 5px #900;
        }}
        h2 {{
            font-size: 30px;
            margin-bottom: 20px;
        }}
        p {{
            font-size: 18px;
        }}
        a {{
            text-decoration: none;
            color: #0066cc;
            font-weight: bold;
        }}
        img {{
            max-width: 400px;
            margin-top: 20px;
        }}
        ul {{
            list-style-type: none;
            padding: 0;
            text-align: left;
            display: inline-block;
            margin-top: 20px;
        }}
        div.logger {{
            margin-top: 30px;
            color: green;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <h1>404</h1>
    <h2>Упс! Страница не найдена 😢</h2>
    <p>IP текущего пользователя: {user_ip}</p>
    <p>Дата и время доступа: {now.strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><a href="{home_url}">Вернуться на главную страницу</a></p>
    <img src="{url_for('static', filename='not_found.png')}" alt="404 картинка">
    
    <div class="logger">
        <h3>Журнал посещений 404:</h3>
        <ul>
            {logs_html}
        </ul>
    </div>
</body>
</html>
''', 404


@app.errorhandler(500)
def handle_500(err):
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Ошибка 500</title>
    <style>
        body { text-align:center; font-family: Arial, sans-serif; background-color: #f2f2f2; }
        h1 { font-size: 150px; color: red; }
        h2 { font-size: 30px; margin-top: 0; }
    </style>
</head>
<body>
    <main>
        <h1>500</h1>
        <h2>Внутренняя ошибка сервера</h2>
        <p>Что-то пошло не так на сервере. Пожалуйста, попробуйте позже.</p>
    </main>
</body>
</html>
''', 500

