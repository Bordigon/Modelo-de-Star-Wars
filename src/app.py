"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favourites
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import session
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def handle_user_list():
    users = db.session.execute(select(User)).scalars().all()
    user_list = []
    for person in users:
        person = User.serialize_only_Name_id(person)
        user_list.append(person)
    return jsonify(user_list), 200


# ------------------------------Devuelve todos los character que hay
@app.route('/people', methods=['GET'])
def handle_people_list():
    peoples = db.session.execute(select(Character)).scalars().all()
    people_list = []
    for person in peoples:
        person = Character.serialize_only_Name_id(person)
        people_list.append(person)
    return jsonify(people_list), 200


# ---------------------------Devuelve la info de un character en particular
@app.route('/people/<int:character_id>', methods=['GET'])
def handle_people(character_id):
    people = db.session.get(Character, character_id)
    if people == None:
        return jsonify("No existe ese personaje")
    people = Character.serialize(people)
    return jsonify(people), 200


# -----------------------------------Devuelve la lista de planetas
@app.route('/planets', methods=['GET'])
def handle_planet_list():
    planets = db.session.execute(select(Planet)).scalars().all()
    planet_list = []
    for planeta in planets:
        planeta = Planet.serialize_only_Name_id(planeta)
        planet_list.append(planeta)
    return jsonify(planet_list), 200


# -------------------------------Devuelve la info de un character en particular
@app.route('/planets/<int:planets_id>', methods=['GET'])
def handle_planet(planets_id):
    planeta = db.session.get(Planet, planets_id)
    if planeta == None:
        return jsonify("No existe ese planeta")
    planeta = Planet.serialize(planeta)
    return jsonify(planeta), 200


# ---------------------------El usuario actual será hasta nuevo aviso, usuario 1
@app.route('/users/favourites', methods=['GET'])
def handle_your_favourites():
    your_favourites = db.session.execute(
        select(Favourites).where(Favourites.user_id == 1)).scalars().all()
    list_of_favourist = []
    for fav in your_favourites:
        list_of_favourist.append(Favourites.serialize(fav))
    return jsonify(list_of_favourist)


# ----------------------------Añade un nuevo planeta a favoritos
@app.route('/favourite/planet/<int:new_planet_id>', methods=['POST'])
def handle_add_planet_to_favs(new_planet_id):
    planet = db.session.get(Planet, new_planet_id)
    if planet == None:
        return jsonify("El planeta que quieres añadir a favoritos, no existe")
    ur_favs = db.session.execute(select(Favourites).where(
        and_(Favourites.user_id == 1, Favourites.planet_id == new_planet_id))).scalars().all()
    if ur_favs != []:
        return jsonify("Ya ese planeta esta agregado en favoritos")
    new_fav = Favourites()
    new_fav.user_id = 1
    new_fav.planet_id = new_planet_id
    db.session.add(new_fav)
    db.session.commit()
    return handle_your_favourites()


# --------------------------Elimina uno de los planetas de favoritos
@app.route('/favourite/planet/<int:old_planet_id>', methods=['DELETE'])
def handle_delete_planet_from_fav(old_planet_id):
    planet = db.session.get(Planet, old_planet_id)
    if planet == None:
        return jsonify("El planeta que quieres eliminar de favoritos, no existe")
    ur_favs = db.session.execute(select(Favourites).where(
        and_(Favourites.user_id == 1, Favourites.planet_id == old_planet_id))).scalars().all()
    print(ur_favs)
    if ur_favs == []:
        return jsonify("Ese planeta ni siquiera lo tienes en favoritos")
    print("hola")
    db.session.delete(ur_favs[0])
    db.session.commit()
    return handle_your_favourites()


# ----------------------------Añade un nuevo personaje a favoritos
@app.route('/favourite/people/<int:new_character_id>', methods=['POST'])
def handle_add_character_to_favs(new_character_id):
    person = db.session.get(Character, new_character_id)
    if person == None:
        return jsonify("El personaje que quieres añadir a favoritos, no existe")
    ur_favs = db.session.execute(select(Favourites).where(
        and_(Favourites.user_id == 1, Favourites.character_id == new_character_id))).scalars().all()
    if ur_favs != []:
        return jsonify("Ya ese personaje esta agregado en favoritos")
    new_fav = Favourites()
    new_fav.user_id = 1
    new_fav.character_id = new_character_id
    db.session.add(new_fav)
    db.session.commit()
    return handle_your_favourites()


# --------------------------Elimina uno de los personajes de favoritos
@app.route('/favourite/people/<int:old_people_id>', methods=['DELETE'])
def handle_delete_character_from_fav(old_people_id):
    person = db.session.get(Character, old_people_id)
    if person == None:
        return jsonify("El personaje que quieres eliminar de favoritos, no existe")
    ur_favs = db.session.execute(select(Favourites).where(
        and_(Favourites.user_id == 1, Favourites.character_id == old_people_id))).scalars().all()
    print(ur_favs)
    if ur_favs == []:
        return jsonify("Ese personaje ni siquiera lo tienes en favoritos")
    db.session.delete(ur_favs[0])
    db.session.commit()
    return handle_your_favourites()


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
