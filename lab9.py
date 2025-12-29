from flask import Blueprint, render_template, request, jsonify, session, redirect
import random

lab9 = Blueprint("lab9", __name__)


BOX_COUNT = 10
AUTH_ONLY_BOXES = {7, 8, 9}   # эти коробки только для авторизованных


_opened_boxes_global = set()
_boxes_layout = None


GREETINGS = [
    "С Новым годом! Пусть мечты сбываются!",
    "Счастья и радости!",
    "Здоровья в новом году!",
    "Пусть мечты сбываются!",
    "Удачи и успехов!",
    "Пусть всё получится!",
    "Много улыбок!",
    "Этот подарок только для своих 🙂",
    "Подарок для авторизованных 🎅",
    "Самый секретный подарок 🎁",
]

GIFT_IMAGES = [f"lab9/gift{i}.png" for i in range(1, BOX_COUNT + 1)]


def is_logged_in():
    return bool(session.get("login"))

def ensure_session():
    if "opened_count" not in session:
        session["opened_count"] = 0

def init_layout_once():
    global _boxes_layout
    if _boxes_layout is not None:
        return

    rnd = random.Random(2025)
    _boxes_layout = []
    for i in range(BOX_COUNT):
        _boxes_layout.append({
            "id": i,
            "top": rnd.randint(15, 75),
            "left": rnd.randint(5, 90),
        })


@lab9.route("/lab9/")
def index():
    init_layout_once()
    ensure_session()

    return render_template(
        "lab9/index.html",
        boxes=_boxes_layout,
        box_count=BOX_COUNT,
        closed_count=BOX_COUNT - len(_opened_boxes_global),
        opened_count=session["opened_count"],
        opened_global=list(_opened_boxes_global),
        is_logged_in=is_logged_in(),
    )

@lab9.route("/lab9/api/open", methods=["POST"])
def open_box():
    ensure_session()
    data = request.get_json(silent=True) or {}
    box_id = data.get("id")

    if not isinstance(box_id, int) or box_id < 0 or box_id >= BOX_COUNT:
        return jsonify({"ok": False, "error": "Некорректная коробка"}), 400

    if box_id in AUTH_ONLY_BOXES and not is_logged_in():
        return jsonify({
            "ok": False,
            "authRequired": True,
            "message": "Этот подарок доступен только после входа"
        })

    if box_id in _opened_boxes_global:
        return jsonify({
            "ok": True,
            "alreadyOpened": True,
            "remaining": BOX_COUNT - len(_opened_boxes_global),
            "openedCount": session["opened_count"],
        })

    if session["opened_count"] >= 3:
        return jsonify({
            "ok": False,
            "limitReached": True,
            "message": "Можно открыть не больше 3 коробок"
        })

    _opened_boxes_global.add(box_id)
    session["opened_count"] += 1

    return jsonify({
        "ok": True,
        "greeting": GREETINGS[box_id],
        "giftImage": GIFT_IMAGES[box_id],
        "remaining": BOX_COUNT - len(_opened_boxes_global),
        "openedCount": session["opened_count"],
    })


@lab9.route("/lab9/api/santa", methods=["POST"])
def santa():
    if not is_logged_in():
        return jsonify({"ok": False, "message": "Нужно войти"}), 403

    _opened_boxes_global.clear()
    return jsonify({"ok": True, "message": "🎅 Дед Мороз наполнил коробки!"})


@lab9.route("/lab9/login12", methods=["GET", "POST"])
def login12():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        if login == "admin" and password == "123":
            session["login"] = login
            return redirect("/lab9/")
        else:
            return render_template(
                "lab9/login12.html",
                error="Неверный логин или пароль"
            )

    return render_template("lab9/login12.html")


@lab9.route("/lab9/register12", methods=["GET", "POST"])
def register12():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        if not login or not password:
            return render_template(
                "lab9/register12.html",
                error="Заполните все поля"
            )

        session["login"] = login
        return redirect("/lab9/")

    return render_template("lab9/register12.html")


@lab9.route("/lab9/logout")
def logout():
    session.clear()
    return redirect("/lab9/")
