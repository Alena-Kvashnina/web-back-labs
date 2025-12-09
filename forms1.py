from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=3)])
    submit = SubmitField("Войти")

class EmployeeForm(FlaskForm):
    full_name = StringField("ФИО", validators=[DataRequired()])
    position = StringField("Должность", validators=[DataRequired()])
    gender = StringField("Пол", validators=[DataRequired()])
    phone = StringField("Телефон")
    email = StringField("Email", validators=[Email()])
    probation = BooleanField("Испытательный срок")
    hire_date = DateField("Дата устройства", format="%Y-%m-%d")
    submit = SubmitField("Сохранить")
