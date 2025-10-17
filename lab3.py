from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab33():
    name = request.cookies.get('name')
    age = request.cookies.get('age')
    name_color = request.cookies.get('name_color')

    # если нет имени или возраста — заменим на значения по умолчанию
    if not name:
        name = 'Аноним'
    if not age:
        age = 'неизвестен'

    return render_template('lab3/lab3.html', name=name, age=age, name_color=name_color)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/clear_cookie')
def clear_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', '', expires=0)
    resp.set_cookie('age', '', expires=0)
    resp.set_cookie('name_color', '', expires=0)
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if not age:
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)



@lab3.route('/lab3/order')
def order():
    return render_template('/lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, черный чай 80 рублей, зеленый 70 рублей
    if drink == 'cofee':
        price = 120
    if drink == 'black-tea':
        price = 80
    if drink == 'green-tea':
        price = 70

    # Добавка молока удорожает напиток за 30 рублей, а сахар на 10
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('/lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        color = request.form.get('color')
        bg_color = request.form.get('bg_color')
        font_size = request.form.get('font_size')
        font_weight = request.form.get('font_weight')

        resp = make_response(redirect('/lab3/settings'))

        if color:
            resp.set_cookie('color', color, max_age=30*24*60*60)
        if bg_color:
            resp.set_cookie('bg_color', bg_color, max_age=30*24*60*60)
        if font_size:
            resp.set_cookie('font_size', font_size, max_age=30*24*60*60)
        if font_weight:
            resp.set_cookie('font_weight', font_weight, max_age=30*24*60*60)

        return resp

    # GET: подставляем текущие значения из куки
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    font_weight = request.cookies.get('font_weight')

    return render_template('lab3/settings.html',
                           color=color, bg_color=bg_color,
                           font_size=font_size, font_weight=font_weight)
# Страница с формой билета
@lab3.route('/lab3/ticket')
def ticket_form():
    return render_template('lab3/ticket_form.html', errors={}, form_data={})


# Обработка формы и генерация билета
@lab3.route('/lab3/ticket', methods=['POST'])
def ticket_submit():
    errors = {}
    form_data = {
        'fio': request.form.get('fio', '').strip(),
        'shelf': request.form.get('shelf'),
        'linen': request.form.get('linen'),
        'baggage': request.form.get('baggage'),
        'age': request.form.get('age'),
        'from_city': request.form.get('from_city', '').strip(),
        'to_city': request.form.get('to_city', '').strip(),
        'date': request.form.get('date'),
        'insurance': request.form.get('insurance')
    }

    # Проверка заполненности полей
    for key, value in form_data.items():
        if key not in ['linen', 'baggage', 'insurance'] and (value is None or value == ''):
            errors[key] = 'Заполните поле!'

    # Проверка возраста
    try:
        age_int = int(form_data['age'])
        if age_int < 1 or age_int > 120:
            errors['age'] = 'Возраст должен быть от 1 до 120'
    except:
        errors['age'] = 'Укажите корректный возраст'

    if errors:
        return render_template('lab3/ticket_form.html', errors=errors, form_data=form_data)

    # Расчёт стоимости
    price = 700 if age_int < 18 else 1000
    if form_data['shelf'] in ['нижняя', 'нижняя боковая']:
        price += 100
    if form_data['linen']:
        price += 75
    if form_data['baggage']:
        price += 250
    if form_data['insurance']:
        price += 150

    ticket_type = 'Детский билет' if age_int < 18 else 'Взрослый билет'

    return render_template('lab3/ticket.html', data=form_data, price=price, ticket_type=ticket_type)


@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.set_cookie('color', '', expires=0)
    resp.set_cookie('bg_color', '', expires=0)
    resp.set_cookie('font_size', '', expires=0)
    resp.set_cookie('font_weight', '', expires=0)
    return resp


# Список товаров
products = [
    {"name": "iPhone 14", "price": 95000, "brand": "Apple", "color": "черный"},
    {"name": "Samsung Galaxy S23", "price": 87000, "brand": "Samsung", "color": "белый"},
    {"name": "Xiaomi 13", "price": 53000, "brand": "Xiaomi", "color": "синий"},
    {"name": "Google Pixel 7", "price": 72000, "brand": "Google", "color": "черный"},
    {"name": "OnePlus 11", "price": 65000, "brand": "OnePlus", "color": "зеленый"},
    {"name": "Huawei P60", "price": 60000, "brand": "Huawei", "color": "черный"},
    {"name": "Honor Magic 5", "price": 54000, "brand": "Honor", "color": "серый"},
    {"name": "iPhone 13", "price": 78000, "brand": "Apple", "color": "синий"},
    {"name": "Samsung A54", "price": 35000, "brand": "Samsung", "color": "фиолетовый"},
    {"name": "Xiaomi Redmi Note 12", "price": 23000, "brand": "Xiaomi", "color": "черный"},
    {"name": "Realme GT 2", "price": 41000, "brand": "Realme", "color": "белый"},
    {"name": "Poco F5", "price": 37000, "brand": "Poco", "color": "синий"},
    {"name": "iPhone SE", "price": 45000, "brand": "Apple", "color": "красный"},
    {"name": "Samsung Z Flip", "price": 89000, "brand": "Samsung", "color": "черный"},
    {"name": "Xiaomi 12T", "price": 47000, "brand": "Xiaomi", "color": "серый"},
    {"name": "Google Pixel 6a", "price": 52000, "brand": "Google", "color": "белый"},
    {"name": "Honor X9", "price": 30000, "brand": "Honor", "color": "золотой"},
    {"name": "Realme 11 Pro", "price": 28000, "brand": "Realme", "color": "черный"},
    {"name": "Poco X5", "price": 25000, "brand": "Poco", "color": "зеленый"},
    {"name": "Huawei Nova 11", "price": 48000, "brand": "Huawei", "color": "серебристый"}
]

min_price_all = min([p['price'] for p in products])
max_price_all = max([p['price'] for p in products])


@lab3.route('/lab3/products')
def products_list():
    min_price_cookie = request.cookies.get('min_price')
    max_price_cookie = request.cookies.get('max_price')

    min_price = request.args.get('min_price') or min_price_cookie
    max_price = request.args.get('max_price') or max_price_cookie

    filtered_products = products

    if min_price or max_price:
        try:
            min_price_val = int(min_price) if min_price else min_price_all
            max_price_val = int(max_price) if max_price else max_price_all

            if min_price_val > max_price_val:
                min_price_val, max_price_val = max_price_val, min_price_val

            filtered_products = [
                p for p in products if min_price_val <= p['price'] <= max_price_val
            ]
        except ValueError:
            min_price_val = min_price_all
            max_price_val = max_price_all
            filtered_products = products
    else:
        min_price_val = ''
        max_price_val = ''

    resp = make_response(render_template(
        'lab3/products.html',
        products=filtered_products,
        min_price=min_price_val,
        max_price=max_price_val,
        min_placeholder=min_price_all,
        max_placeholder=max_price_all,
        total=len(filtered_products)
    ))

    if min_price:
        resp.set_cookie('min_price', str(min_price_val), max_age=60*60*24*30)
    if max_price:
        resp.set_cookie('max_price', str(max_price_val), max_age=60*60*24*30)

    return resp


@lab3.route('/lab3/products/reset')
def products_reset():
    resp = make_response(
        render_template(
            'lab3/products.html',
            products=products,
            min_price='',
            max_price='',
            min_placeholder=min_price_all,
            max_placeholder=max_price_all,
            total=len(products)
        )
    )
    resp.set_cookie('min_price', '', expires=0)
    resp.set_cookie('max_price', '', expires=0)
    return resp