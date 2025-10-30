from flask import Blueprint, render_template, request, redirect
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab44():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods=['GET', 'POST'])
def div():
    if request.method == 'GET':
        return render_template('lab4/div.html')

    # Если POST — обрабатываем данные
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    # Проверка на пустые значения
    if not x1 or not x2:
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    # Преобразование в числа с обработкой ошибок
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/div.html', error='Введите корректные числа!')

    # Проверка на деление на ноль
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')

    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum', methods=['GET', 'POST'])
def sum():
    if request.method == 'GET':
        return render_template('lab4/sum.html')

    x1 = request.form.get('x1') or 0
    x2 = request.form.get('x2') or 0

    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/sum.html', error='Введите корректные числа!')

    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul', methods=['GET', 'POST'])
def mul():
    if request.method == 'GET':
        return render_template('lab4/mul.html')

    x1 = request.form.get('x1') or 1
    x2 = request.form.get('x2') or 1

    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/mul.html', error='Введите корректные числа!')

    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub', methods=['GET', 'POST'])
def sub():
    if request.method == 'GET':
        return render_template('lab4/sub.html')

    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if not x1 or not x2:
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')

    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/sub.html', error='Введите корректные числа!')

    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/pow', methods=['GET', 'POST'])
def pow_view():
    if request.method == 'GET':
        return render_template('lab4/pow.html')

    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    # Ошибка при пустых полях
    if not x1 or not x2:
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')

    try:
        a = float(x1)
        b = float(x2)
    except ValueError:
        return render_template('lab4/pow.html', error='Введите корректные числа!')

    # Явная проверка 0^0 — до вычисления, чтобы не полагаться на поведение Python
    if a == 0 and b == 0:
        return render_template('lab4/pow.html', error='0^0 — неопределённость!')

    try:
        result = a ** b
    except OverflowError:
        return render_template('lab4/pow.html', error='Результат слишком большой!')
    except Exception as e:
        return render_template('lab4/pow.html', error=f'Ошибка при вычислении: {e}')

    return render_template('lab4/pow.html', x1=a, x2=b, result=result)


tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
  
    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1

    return redirect('/lab4/tree')

