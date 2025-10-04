from flask import  Blueprint, url_for, redirect, request, abort, render_template
import datetime
lab2 = Blueprint('lab2', __name__)


flowers = []   # теперь пустой список при старте


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers_one(flower_id):
    if flower_id < 0 or flower_id >= len(flowers):
        abort(404)
    return render_template('flower.html', flower=flowers[flower_id], flower_id=flower_id, total=len(flowers))


@lab2.route('/lab2/all_flowers')
def all_flowers():
    return render_template('flowers.html', flowers=flowers)


@lab2.route('/lab2/add_flower', methods=['POST'])
def add_flower():
    name = request.form.get("name")
    price = request.form.get("price")

    if not name or not price:
        return "Нужно указать и название, и цену цветка", 400

    try:
        price = int(price)
    except ValueError:
        return "Цена должна быть числом", 400

    flowers.lab2end({"name": name, "price": price})
    return redirect(url_for("all_flowers"))


@lab2.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flowers):
        abort(404)
    flowers.pop(flower_id)
    return redirect(url_for("all_flowers"))


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flowers.clear()
    return redirect(url_for("all_flowers"))


@lab2.route('/lab2/example')
def example():
    name = 'Квашнина Алёна'
    group = 'ФБИ-34'
    lab_num = 2
    course = 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321},
        ]
    return render_template('example.html', 
                           name=name, group=group, lab_num= lab_num,
                           course=course, fruits=fruits)


@lab2.route('/lab2/')
def lab2():
    routes = [
        {'name': 'Пример с фруктами', 'url': url_for('example')},
        {'name': 'Фильтры Jinja2', 'url': url_for('filters')},
        {'name': 'Калькулятор (по умолчанию 1/1)', 'url': url_for('calc_default')},
        {'name': 'Калькулятор (7 и 1)', 'url': url_for('calc_one_arg', a=7)},
        {'name': 'Калькулятор (3 и 4)', 'url': url_for('calc', a=3, b=4)},
        {'name': 'Цветок №0', 'url': url_for('flowers', flower_id=0)},
        {'name': 'Список всех цветов', 'url': url_for('all_flowers')},
        {'name': 'Добавить цветок', 'url': url_for('add_flower', name='роза')},
        {'name': 'Очистить список цветов', 'url': url_for('clear_flowers')},
        {'name': 'Список книг', 'url': url_for('books')},
        {'name': 'Список ягод с картинками', 'url': url_for('berries')},
    ]
    return render_template('lab2.html', routes=routes)


@lab2.route('/lab2/filters')
def filters():
    phrase = "0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...."
    return render_template('filter.html', phrase = phrase)


@lab2.route('/lab2/calc/')
def calc_default():
    # по умолчанию пересылаем на /lab2/calc/1/1
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
def calc_one_arg(a):
    # пересылаем на /lab2/calc/a/1
    return redirect(f'/lab2/calc/{a}/1')


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    # защита от деления на ноль
    division = "∞" if b == 0 else round(a / b, 2)

    return f'''
<!doctype html>
<html>
    <body>
        <h1>Расчёт с параметрами:</h1>
        <p>{a} + {b} = {a + b}</p>
        <p>{a} - {b} = {a - b}</p>
        <p>{a} × {b} = {a * b}</p>
        <p>{a} / {b} = {division}</p>
        <p>{a}<sup>{b}</sup> = {a ** b}</p>
    </body>
</html>
'''


@lab2.route('/lab2/books')
def books():
    books_list = [
        {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 672},
        {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман", "pages": 1225},
        {"author": "Александр Пушкин", "title": "Евгений Онегин", "genre": "Роман в стихах", "pages": 320},
        {"author": "Антон Чехов", "title": "Вишнёвый сад", "genre": "Пьеса", "pages": 112},
        {"author": "Николай Гоголь", "title": "Мёртвые души", "genre": "Поэма", "pages": 352},
        {"author": "Иван Тургенев", "title": "Отцы и дети", "genre": "Роман", "pages": 280},
        {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Роман", "pages": 480},
        {"author": "Максим Горький", "title": "Мать", "genre": "Роман", "pages": 416},
        {"author": "Александр Куприн", "title": "Олеся", "genre": "Повесть", "pages": 160},
        {"author": "Владимир Набоков", "title": "Лолита", "genre": "Роман", "pages": 368}
    ]
    return render_template("books.html", books=books_list)


@lab2.route('/lab2/berries')
def berries():
    berries_list = [
        {"name": "Клубника", "desc": "Сочная и сладкая летняя ягода.", "img": url_for('static', filename='berries.klubnika.jpg')},
        {"name": "Малина", "desc": "Ароматная ягода с кислинкой.", "img": url_for('static', filename='berries.malina.jpg')},
        {"name": "Черника", "desc": "Полезная ягода для зрения.", "img": url_for('static', filename='berries.chernika.jpg')},
        {"name": "Смородина", "desc": "Черная или красная, богата витамином C.", "img": url_for('static', filename='berries.smorodina.jpg')},
        {"name": "Голубика", "desc": "Лесная ягода, похожа на чернику, но крупнее.", "img": url_for('static', filename='berries.golubika.jpg')},
        {"name": "Ежевика", "desc": "Колючая, но очень вкусная ягода.", "img": url_for('static', filename='berries.ezhevika.jpg')},
        {"name": "Брусника", "desc": "Ягода северных лесов, хороша для морса.", "img": url_for('static', filename='berries.brusnika.jpg')},
        {"name": "Клюква", "desc": "Кислая болотная ягода.", "img": url_for('static', filename='berries.klukva.jpg')},
        {"name": "Облепиха", "desc": "Оранжевые ягоды, из которых делают масло.", "img": url_for('static', filename='berries.oblepikha.jpg')},
        {"name": "Крыжовник", "desc": "Зеленая или красная ягода с кисло-сладким вкусом.", "img": url_for('static', filename='berries.kryzhovnik.jpg')},
        {"name": "Шиповник", "desc": "Ягода дикого розового куста, очень витаминная.", "img": url_for('static', filename='berries.shipovnik.jpg')},
        {"name": "Рябина", "desc": "Красные ягоды, которые любят птицы.", "img": url_for('static', filename='berries.ryabina.jpg')},
        {"name": "Калина", "desc": "Красная горьковатая ягода.", "img": url_for('static', filename='berries.kalina.jpg')},
        {"name": "Жимолость", "desc": "Темно-синие ягоды необычной формы.", "img": url_for('static', filename='berries.zhimolost.jpg')},
        {"name": "Ирга", "desc": "Сладкая ягода, напоминающая чернику.", "img": url_for('static', filename='berries.irga.jpg')},
        {"name": "Барбарис", "desc": "Кислые ягоды, часто используют в конфетах.", "img": url_for('static', filename='berries.barbaris.jpg')},
        {"name": "Черемуха", "desc": "Ягода с терпким вкусом.", "img": url_for('static', filename='berries.cheremukha.jpg')},
        {"name": "Морошка", "desc": "Редкая болотная ягода янтарного цвета.", "img": url_for('static', filename='berries.moroshka.jpg')},
        {"name": "Арония", "desc": "Черноплодная рябина, полезная для давления.", "img": url_for('static', filename='berries.aronia.jpg')},
        {"name": "Вишня", "desc": "Кисло-сладкая ягода для компотов и пирогов.", "img": url_for('static', filename='berries.vishnya.jpg')}
    ]
    return render_template("berries.html", berries=berries_list)

