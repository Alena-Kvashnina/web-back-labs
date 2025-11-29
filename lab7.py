from flask import Blueprint, render_template, request, jsonify

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def lab77():
    return render_template('lab7/index.html')

films = [
    {
        "title": "Time loop",
        "title_ru": "Петля времени",
        "year": 2012,
        "description": "В недалеком будущем, где стали возможны путешествия во времени, \
            некая корпорация убирает нежелательных людей, отправляя их в прошлое. Задача \
            принимающей стороны — убить жертву, стерев тем самым несчастного из истории."
    },
    {
        "title": "Little nothings of life",
        "title_ru": "Мелочи жизни",
        "year": 2025,
        "description": "«Мелочи жизни» — художественный фильм режиссёра Тима Милантса. \
            Экранизация одноимённой книги Клэр Киган, попавшей в 2022 году в шорт-лист \
            Букеровской премии. Продюсерами фильма станут Алан Молони и Киллиан Мерфи, \
            который также сыграет в фильме главную роль вместе с Киараном Хайндсом и Эмили Уотсон. "
    },
    {
        "title": "Alpha",
        "title_ru": "Альфа",
        "year": 2018,
        "description": "20 000 лет назад Земля была холодным и неуютным местом, в котором \
            смерть подстерегала человека на каждом шагу, а жизнь зависела от того, удалось \
            ли загнать добычу или нет. Молодой охотник из племени, которое по уровню жизни \
            и культуры было одним из самых развитых на планете, оказывается один на один с \
            враждебным миром, полным смертельных опасностей. Ему предстоит заглянуть в лицо \
            своим страхам и найти дорогу домой. И возможно, от исхода его путешествия зависит \
            судьба всего человечества."
    },
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Фильм не найден"}, 404
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Фильм не найден"}, 404
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Фильм не найден"}, 404
    film_data = request.get_json()
    
    if film_data['description'] == "":
        return {'description': 'Заполните описание'}, 400
    
    films[id] = film_data
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film_data = request.get_json()
    
    if film_data['description'] == "":
        return {'description': 'Заполните описание'}, 400
    
    films.append(film_data)
    return jsonify({"id": len(films) - 1}), 201