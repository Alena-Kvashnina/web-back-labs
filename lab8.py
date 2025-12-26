from flask import Blueprint, render_template, session, request, redirect
from db import db
from db.models import users, articles


lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab88():  
    return render_template('lab8/lab8.html', username='Anonymous')

@lab8.route('/lab8/login')
def login():
    return "Страница входа"

@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')
    

    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect('/lab8/')


@lab8.route('/lab8/articles')
def articles():
    return "Список статей"

@lab8.route('/lab8/create')
def create():
    return "Создать статью"