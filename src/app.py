"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People , Planets ,FavoritePeople,FavoritePlanets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
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
def handle_user():
    
        user = User.query.all()
        user = list(map(lambda item: item.serialize(), user))

        return jsonify({
            "data": user
        }), 200


@app.route('/user-id/<int:id>', methods=['GET'])
def handle_user_id(id):
    
        user = User.query.get(id)
        

        return jsonify({
            "data": user.serialize()
        }), 200


@app.route('/people', methods=['GET'])
def handle_people():
    if request.method == 'GET':
        people = People.query.all()
        people = list(map(lambda item: item.serialize(), people))

        return jsonify({
            "data": people
        }), 200
    
@app.route('/people-id/<int:id>', methods=['GET'])
def handle_people_id(id):
    if request.method == 'GET':
        people = People.query.get(id)
        

        return jsonify({
            "data": people.serialize()
        }), 200    
   

@app.route('/planets', methods=['GET'])
def handle_planets():
    
        planets = Planets.query.all()
        planets = list(map(lambda item: item.serialize(), planets))

        return jsonify({
            "data": planets
        }), 200
    
@app.route('/planet-id/<int:id>', methods=['GET'])
def handle_planets_id(id):
        
        planets = Planets.query.get(id)
        
        return jsonify({
            "data": planets.serialize()
        }), 200   


@app.route('/planets/favorite/<int:planets_id>', methods=["POST"])
def post_fav_planet(planets_id):
    one = Planets.query.get(planets_id)
    user = User.query.get(1)
    if one is None:
        return jsonify({"error": "The planet does not exist"}), 404

    existing_favorite = FavoritePlanets.query.filter_by(user_id=user.id, planets_id=planets_id).first()
    if existing_favorite:
        return jsonify({"message": "Favorite already exists"}), 400

    try:
        new_fav = FavoritePlanets(user_id=user.id, planets_id=planets_id)
        db.session.add(new_fav)
        db.session.commit()
        return jsonify({"message": "Favorite planet added"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Failed to add favorite"}), 500
    


@app.route('/people/favorite/<int:people_id>', methods=["POST"])
def post_fav_people(people_id):
    one = People.query.get(people_id)
    user = User.query.get(1)
    if one is None:
        return jsonify({"error": "People not exist"}), 404

    existing_favorite = FavoritePeople.query.filter_by(user_id=user.id, people_id=people_id).first()
    if existing_favorite:
        return jsonify({"message": "Favorite already exists"}), 400

    try:
        new_fav = FavoritePeople(user_id=user.id, people_id=people_id)
        db.session.add(new_fav)
        db.session.commit()
        return jsonify({"message": "Favorite people added"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Failed to add favorite"}), 500
    

@app.route("/planets/favorite/<int:planet_id>", methods=["DELETE"])
def delete_fav_planet(planet_id):
    one = FavoritePlanets.query.filter_by(planets_id=planet_id).first()
    if(one):
        db.session.delete(one)
        db.session.commit()
        return jsonify({
        "message": "The planet with id=" + str(planet_id) + " was dleted"
    })
    else:
        raise APIException("The planet does not exist", status_code=404)


@app.route("/people/favorite/<int:people_id>", methods=["DELETE"])
def delete_fav_people(people_id):
    one = FavoritePeople.query.filter_by(people_id=people_id).first()
    if(one):
        db.session.delete(one)
        db.session.commit()
        return jsonify({
        "mensaje": "People with id=" + str(people_id) + " was deleted"
    })
    else:
        raise APIException("People do not exist", status_code=404)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
