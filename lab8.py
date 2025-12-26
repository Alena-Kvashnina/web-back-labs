from flask import Blueprint, render_template, request, make_response, redirect, session, current_app, abort, jsonify
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user
import psycopg2
from datetime import datetime
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from flask_login import logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import func 

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab88():  
    return render_template('lab8/lab8.html', username='Anonymous')

login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('check') == 'on'
    
    if not login_form or not login_form.strip():
        return render_template('lab8/login.html', error='Введите логин!')
    if not password_form or not password_form.strip():
        return render_template('lab8/login.html', error='Введите пароль!')
    
    user = users.query.filter_by(login = login_form).first()
    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember = remember)
            return redirect('/lab8/')

    return render_template('lab8/login.html', error='Ошибка входа: логин и/или пароль неверны')

    

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

@lab8.route('/lab8/articles/')
def article_list():
    query = request.args.get('query', '').strip().lower()
    
    if not current_user.is_authenticated:
        base_query = articles.query.filter(articles.is_public == 1)
    else:
        base_query = articles.query.filter(
            (articles.is_public == 1) | (articles.login_id == current_user.id)
        )
    
    all_articles = base_query.all()
    
    if not query:
        articles_list = all_articles
    else:
        articles_list = []
        for article in all_articles:
            title_lower = article.title.lower() if article.title else ""
            text_lower = article.article_text.lower() if article.article_text else ""
            
            if query in title_lower or query in text_lower:
                articles_list.append(article)
    
    return render_template('lab8/articles.html', articles=articles_list, query=query)


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/create')
def create():
    return "Создать статью"