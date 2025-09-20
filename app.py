from flask import Flask, url_for, request, redirect, abort
import datetime
app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    lab1_web = url_for("web")
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
            </ul>
        </main>
        <footer>
            <hr>
            <p>Квашнина Алёна Юрьевна, ФБИ-34, 3 курс, 2025 год</p>
        </footer>
    </body>
</html>
'''
@app.route("/lab1/")
def lab1():
    title_page = url_for('title_page')
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Лабораторная 1</title>
</head>
<body>
    <main>
        <p>Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые ба-
        зовые возможности.</p>

        <br><a href="''' + title_page + '''">Назад в главное меню</a>

        <h2>Список роутов</h2>

        <ul>
            <li><a href="/lab1/web">/lab1/web</a></li>
            <li><a href="/lab1/author">/lab1/author</a></li>
            <li><a href="/lab1/image">/lab1/image</a></li>
            <li><a href="/lab1/counter">/lab1/counter</a></li>
            <li><a href="/lab1/counter/clear">/lab1/counter/clear</a></li>
            <li><a href="/lab1/info">/lab1/info</a></li>
            <li><a href="/lab1/create">/lab1/create</a></li>
            <li><a href="/lab1/400">/lab1/400</a></li>
            <li><a href="/lab1/401">/lab1/401</a></li>
            <li><a href="/lab1/402">/lab1/402</a></li>
            <li><a href="/lab1/403">/lab1/403</a></li>
            <li><a href="/lab1/405">/lab1/405</a></li>
            <li><a href="/lab1/418">/lab1/418</a></li>
            <li><a href="/lab1/500">/lab1/500</a></li>
            <li><a href="/lab1/aboba">Несуществующая страница</a></li>
        </ul>

    </main>
</body>
</html>
'''

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404 

@app.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html>
            <body>
                <h1>web-сервер на flask</h1>
            </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }
        
@app.route("/lab1/author")
def author():
    name = "Квашнина Алёна Юрьевна"
    group = "ФБИ-34"
    faculty = "ФБ"

    return """<!doctype html>
       <html>
           <body>
              <p>Студент: """ + name + """</p>
              <p>Группа: """ + group + """</p>
              <p>Факультет: """ + faculty + """</p>
              <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/image")
def image():

    path = url_for("static", filename = "oak.jpg")
    style = url_for("static", filename = "lab1.css")

    return'''<!doctype html>
        <html>
           <head>
               <link rel="stylesheet" href="''' + style + '''">
           </head>
           <body>
               <h1>Дуб</h1>
                <img src="''' + path + '''">
           </body>
        </html>''', 200, {
            'Content-Language': 'ru',
            'X-Img-Name': 'oak',
            'X-Hotel': 'Trivago'
        }


count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    client_ip = request.remote_addr

    return '''<!doctype html> 
        <html>
            <body>
                Сколько раз вы сюда заходили: ''' + str(count) + '''
                <hr>
                <br> Дата и время: ''' + time + '''
                <br> Запрошенный адрес: ''' + url + '''
                <br> Ваш IP адрес: ''' + client_ip + '''
                <br><a href="/lab1/counter/reset">Сбросить счётчик</a>
            </body>
        </html>'''

@app.route('/lab1/counter/reset')
def reset_counter():
    global count
    count = 0
    return '''<!doctype html>
        <html>
            <body>
                <h1>Счётчик обнулён!</h1>
                <a href="/lab1/counter">Назад к счётчику</a>
            </body>
        </html>'''

@app.route('/lab1/info')
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return ''' 
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

@app.route("/lab1/400")
def error_400():
    return "Некорректный запрос", 400

@app.route("/lab1/401")
def error_401():
    return "Пользователь не авторизован", 401

@app.route("/lab1/402")
def error_402():
    return "Необходима оплата", 402

@app.route("/lab1/403")
def error_403():
    return "Доступ закрыт", 403

@app.route("/lab1/405")
def error_405():
    return "Метод не поддерживается", 405

@app.route("/lab1/418")
def error_418():
    return "Я чайник", 418

@app.route("/lab1/500")
def error_500():

    a = 0
    b = 100

    return b/a

logger = []

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

@app.route('/lab2/a/')
def a():
    return 'ok'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return "цветок: " + flower_list[flower_id]
    
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен цветок</h1>
    <p>Название нового цветка: {name}</p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''
