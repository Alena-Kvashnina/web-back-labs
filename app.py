from flask import Flask, url_for, request, redirect
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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

@app.route('/lab1/image')
def image():
    path = url_for("static", filename="oak.jpg")
    css = url_for("static", filename="lab1.css")
    return '''<!doctype html> 
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + css + '''">
            </head>
            <body>
                <h1>Дуб</h1>
                <img src="''' + path + '''">
            </body>
        </html>'''

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

