from flask import Flask, url_for, render_template, request
import datetime
import os
from os import path
from flask_login import LoginManager

# Импортируем db из нашего модуля db
from db import db
from db.models import users  # для LoginManager

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9

app = Flask(__name__)

# Инициализация LoginManager ПЕРВОЙ!
login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

# НАСТРОЙКА КОНФИГУРАЦИИ
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Секретно-секретный-секрет')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')  # postgres по умолчанию!

# Настройка подключения к БД
db_type = app.config['DB_TYPE']

if db_type == 'postgres':
    db_name = 'alena_kvashnina_orm'
    db_user = 'alena_kvashnina_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, 'alena_kvashnina_orm.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

# Инициализация БД с приложением
db.init_app(app)

# Создание таблиц
with app.app_context():
    db.create_all()

# РЕГИСТРАЦИЯ BLUEPRINTS
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)

logger = []

@app.route("/")
@app.route("/index")
def index():
    lab1_url = url_for("lab1.lab")
    lab2_url = url_for("lab2.lab22")
    lab3_url = url_for("lab3.lab33")
    lab4_url = url_for("lab4.lab44")
    lab5_url = url_for("lab5.lab55")
    lab6_url = url_for("lab6.lab66")
    lab7_url = url_for("lab7.lab77")
    lab8_url = url_for("lab8.lab88")
    lab9_url = url_for("lab9.index")

    return f'''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>НГТУ, ФБ, Лабораторные работы</title>
</head>
<body>
    <header>
        НГТУ, ФБ, WEB-программирование часть 2
        <hr>
    </header>
    <main>
        <h1>Лабораторные работы по WEB-программированию</h1>

        <div class="menu"> 
            <ul>
                <li><a href="{lab1_url}">Лабораторная работа #1</a></li>
                <li><a href="{lab2_url}">Лабораторная работа #2</a></li>
                <li><a href="{lab3_url}">Лабораторная работа #3</a></li>
                <li><a href="{lab4_url}">Лабораторная работа #4</a></li>
                <li><a href="{lab5_url}">Лабораторная работа #5</a></li>
                <li><a href="{lab6_url}">Лабораторная работа #6</a></li>
                <li><a href="{lab7_url}">Лабораторная работа #7</a></li>
                <li><a href="{lab8_url}">Лабораторная работа #8</a></li>
                <li><a href="{lab9_url}">Лабораторная работа #9</a></li>
            </ul>
        </div>
    </main>
    <footer>
        <hr>
        &copy;Квашнина Алёна Юрьевна, ФБИ-34, 2025
    </footer>
</body>
</html>
'''

# ОБРАБОТЧИКИ ОШИБОК
@app.errorhandler(404)
def not_found(err):
    global logger
    now = datetime.datetime.today()
    logger.append(f"[{now.strftime('%Y-%m-%d %H:%M:%S')} пользователь {request.remote_addr}] перешел по адресу: {request.url}")
    logs = ""
    for i in logger:
        logs += f"<li>{i}</li> "
    
    return f'''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Ошибка 404</title>
    <style>
        h1, h2 {{
            font-size: 200px;
            color: violet;
            text-shadow: 5px 5px 10px purple;
            text-align: center;
            margin-bottom: 0;
            margin-top: 60px;
            animation: float 3s ease-in-out infinite;
        }}

         h2 {{
            font-size: 40px;
            text-shadow: none;
        }}
        ul {{
            list-style-type: none;
        }}
        div.logger {{
            position: fixed;
            bottom: 0px;
            left: 0px;
            color: green;
        }}
    
        @keyframes float {{
        0%   {{ transform: translateY(0px); }}
        50%  {{ transform: translateY(-20px); }}
        100% {{ transform: translateY(0px); }}
        }}

    </style>
</head>
<body>
    <main>
        <h1>404</h1>
        <h2>Страница по запрашиваемому адресу не найдена</h2>
        <div class="logger">
            <ul>
                {logs}
            </ul>
        </div>
    </main>
</body>
</html>
''', 404

@app.errorhandler(500)
def internal_error(err):
    return '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Ошибка 500</title>
</head>
<body style="text-align:center;">
    <h1 style="font-size:120px;color:red;">500</h1>
    <h2>Внутренняя ошибка сервера</h2>
</body>
</html>
''', 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)