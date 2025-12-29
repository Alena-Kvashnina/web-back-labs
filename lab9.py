from flask import Blueprint, render_template

lab8 = Blueprint('lab9', __name__)

@lab8.route('/lab9/')
def lab99():
    return render_template('lab9/index.html')
