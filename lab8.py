from flask import Blueprint, render_template
from flask_login import current_user

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    # Получаем имя пользователя или 'anonymous'
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    return render_template('lab8/lab8.html', username=username)

@lab8.route('/lab8/login')
def login():
    return render_template('lab8/lab8.html', username='anonymous', page='login')

@lab8.route('/lab8/register')
def register():
    return render_template('lab8/lab8.html', username='anonymous', page='register')

@lab8.route('/lab8/articles')
def articles():
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    return render_template('lab8/lab8.html', username=username, page='articles')

@lab8.route('/lab8/create')
def create():
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    return render_template('lab8/lab8.html', username=username, page='create')