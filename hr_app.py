from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models1 import db, User, Employee
from forms1 import LoginForm, EmployeeForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3

hr = Blueprint(
    "hr",
    __name__,
    template_folder="templates/templates1",
    static_folder="static/static1"
)

def is_logged_in():
    return "user_id" in session


@hr.route("/")
def index():
    page = int(request.args.get("page", 1))
    per_page = 20
    search = request.args.get("search", "")
    search_field = request.args.get("search_field", "all")  # Новый параметр
    sort = request.args.get("sort", "id")
    sort_direction = request.args.get("direction", "asc")

    query = Employee.query

    # ПОИСК ПО КОНКРЕТНОМУ ПОЛЮ
    if search:
        search_str = f"%{search}%"
        
        if search_field == "all":
            # Поиск по всем полям
            query = query.filter(
                (Employee.full_name.ilike(search_str)) |
                (Employee.position.ilike(search_str)) |
                (Employee.gender.ilike(search_str)) |
                (Employee.phone.ilike(search_str)) |
                (Employee.email.ilike(search_str)) |
                (Employee.probation == (search.lower() in ['да', 'yes', 'true', '1']))
            )
            # Попытка поиска по дате
            try:
                search_date = datetime.strptime(search, '%Y-%m-%d').date()
                query = query.filter(Employee.hire_date == search_date)
            except ValueError:
                pass
                
        elif search_field == "full_name":
            query = query.filter(Employee.full_name.ilike(search_str))
        elif search_field == "position":
            query = query.filter(Employee.position.ilike(search_str))
        elif search_field == "gender":
            query = query.filter(Employee.gender.ilike(search_str))
        elif search_field == "phone":
            query = query.filter(Employee.phone.ilike(search_str))
        elif search_field == "email":
            query = query.filter(Employee.email.ilike(search_str))
        elif search_field == "probation":
            # Поиск по испытательному сроку
            if search.lower() in ['да', 'yes', 'true', '1', 'испытательный']:
                query = query.filter(Employee.probation == True)
            elif search.lower() in ['нет', 'no', 'false', '0']:
                query = query.filter(Employee.probation == False)
        elif search_field == "hire_date":
            # Поиск по дате
            try:
                search_date = datetime.strptime(search, '%Y-%m-%d').date()
                query = query.filter(Employee.hire_date == search_date)
            except ValueError:
                # Если не удалось распарсить дату, ищем как текст
                query = query.filter(Employee.hire_date.cast(db.String).ilike(search_str))

    # СОРТИРОВКА
    if hasattr(Employee, sort):
        column = getattr(Employee, sort)
        if sort_direction == "desc":
            column = column.desc()
        query = query.order_by(column)

    employees = query.offset((page - 1) * per_page).limit(per_page).all()
    total_count = query.count()
    has_more = total_count > page * per_page

    return render_template("index1.html",
                           employees=employees,
                           page=page,
                           search=search,
                           search_field=search_field,  # Передаем в шаблон
                           sort=sort,
                           direction=sort_direction,
                           has_more=has_more,
                           total_count=total_count)


@hr.route("/load_more", methods=["GET"])
def load_more():
    page = int(request.args.get("page", 1))
    search = request.args.get("search", "")
    search_field = request.args.get("search_field", "all")
    sort = request.args.get("sort", "id")
    direction = request.args.get("direction", "asc")
    
    return redirect(url_for("hr.index", 
                           page=page+1, 
                           search=search, 
                           search_field=search_field,
                           sort=sort, 
                           direction=direction))


@hr.route("/login", methods=["GET", "POST"])
def login():
    if is_logged_in():
        return redirect(url_for("hr.index"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Вы успешно вошли в систему!", "success")
            return redirect(url_for("hr.index"))
        else:
            flash("Неверное имя пользователя или пароль", "error")
    
    return render_template("login1.html", form=form, register=False)


@hr.route("/logout")
def logout():
    session.clear()
    flash("Вы вышли из системы", "info")
    return redirect(url_for("hr.index"))


@hr.route("/employee/add", methods=["GET", "POST"])
def add_employee():
    if not is_logged_in():
        flash("Для добавления сотрудника необходимо войти в систему", "warning")
        return redirect(url_for("hr.login"))

    form = EmployeeForm()
    if form.validate_on_submit():
        emp = Employee(
            full_name=form.full_name.data,
            position=form.position.data,
            gender=form.gender.data,
            phone=form.phone.data or "",
            email=form.email.data or "",
            probation=form.probation.data,
            hire_date=form.hire_date.data
        )
        db.session.add(emp)
        db.session.commit()
        flash(f"Сотрудник {emp.full_name} успешно добавлен!", "success")
        return redirect(url_for("hr.index"))

    return render_template("employee_form1.html", form=form, action="Добавить сотрудника")


@hr.route("/employee/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):
    if not is_logged_in():
        flash("Для редактирования необходимо войти в систему", "warning")
        return redirect(url_for("hr.login"))

    emp = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=emp)

    if form.validate_on_submit():
        emp.full_name = form.full_name.data
        emp.position = form.position.data
        emp.gender = form.gender.data
        emp.phone = form.phone.data or ""
        emp.email = form.email.data or ""
        emp.probation = form.probation.data
        emp.hire_date = form.hire_date.data
        
        db.session.commit()
        flash(f"Данные сотрудника {emp.full_name} обновлены!", "success")
        return redirect(url_for("hr.index"))

    return render_template("employee_form1.html", form=form, action="Редактировать сотрудника")


@hr.route("/employee/delete/<int:id>", methods=["GET", "POST"])
def delete_employee(id):
    if not is_logged_in():
        flash("Для удаления необходимо войти в систему", "warning")
        return redirect(url_for("hr.login"))

    emp = Employee.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(emp)
        db.session.commit()
        flash(f"Сотрудник {emp.full_name} удален!", "info")
        return redirect(url_for("hr.index"))

    return render_template("confirm_delete1.html", employee=emp)


@hr.route("/register", methods=["GET", "POST"])
def register():
    if is_logged_in():
        return redirect(url_for("hr.index"))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        # Проверяем, нет ли уже такого пользователя
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Пользователь с таким именем уже существует", "error")
        else:
            hashed_pw = generate_password_hash(form.password.data)
            user = User(username=form.username.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash("Регистрация успешна! Теперь вы можете войти.", "success")
            return redirect(url_for("hr.login"))
    
    return render_template("login1.html", form=form, register=True)


@hr.route("/generate_test_data", methods=["GET"])
def generate_test_data():
    """Генерация тестовых данных (100+ сотрудников)"""
    if not is_logged_in():
        return redirect(url_for("hr.login"))
    
    from datetime import datetime, timedelta
    import random
    
    positions = ["Менеджер", "Разработчик", "Аналитик", "Дизайнер", "Тестировщик", 
                 "Администратор", "Бухгалтер", "Маркетолог", "HR-специалист", 
                 "Руководитель отдела", "Системный администратор", "Контент-менеджер",
                 "SEO-специалист", "Копирайтер", "Юрист", "Логист"]
    
    genders = ["М", "Ж"]
    
    last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Васильев", 
                  "Попов", "Новиков", "Федоров", "Морозов", "Волков", "Алексеев",
                  "Лебедев", "Семенов", "Егоров", "Павлов", "Козлов", "Степанов"]
    
    first_names_m = ["Александр", "Дмитрий", "Сергей", "Андрей", "Алексей", 
                     "Михаил", "Иван", "Артем", "Кирилл", "Максим", "Владимир",
                     "Павел", "Роман", "Николай", "Егор"]
    
    first_names_f = ["Елена", "Ольга", "Ирина", "Наталья", "Мария", 
                     "Анна", "Екатерина", "Татьяна", "Светлана", "Юлия",
                     "Виктория", "Анастасия", "Дарья", "Ксения", "Маргарита"]
    
    # Удаляем существующих сотрудников
    Employee.query.delete()
    
    # Генерируем 150 сотрудников
    for i in range(150):
        last_name = random.choice(last_names)
        
        if random.choice([True, False]):
            first_name = random.choice(first_names_m)
            gender = "М"
            middle_name = random.choice(["Александрович", "Дмитриевич", "Сергеевич", 
                                         "Андреевич", "Алексеевич", "Иванович"])
        else:
            first_name = random.choice(first_names_f)
            gender = "Ж"
            middle_name = random.choice(["Александровна", "Дмитриевна", "Сергеевна",
                                         "Андреевна", "Алексеевна", "Ивановна"])
        
        emp = Employee(
            full_name=f"{last_name} {first_name} {middle_name}",
            position=random.choice(positions),
            gender=gender,
            phone=f"+7{random.randint(900, 999)}{random.randint(100, 999)}{random.randint(10, 99)}{random.randint(10, 99)}",
            email=f"{last_name.lower()}.{first_name.lower()[0]}{random.randint(1, 99)}@company.ru",
            probation=random.choice([True, False, False, False]),  # Чаще False
            hire_date=datetime.now().date() - timedelta(days=random.randint(1, 365*5))
        )
        
        db.session.add(emp)
    
    db.session.commit()
    
    flash("Сгенерировано 150 тестовых сотрудников!", "success")
    return redirect(url_for("hr.index"))