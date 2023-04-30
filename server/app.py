#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        return make_response(jsonify({'message': 'Welcome to the Plants API'}), 200)
    
api.add_resource(Home, '/')

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])
    
    def post(self):
        plant = Plant(**request.get_json())
        db.session.add(plant)
        db.session.commit()
        return jsonify(plant.to_dict())
    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get(plant_id)
        return jsonify(plant.to_dict())
    
    def put(self, plant_id):
        plant = Plant.query.get(plant_id)
        data = request.get_json()
        plant.name = data['name']
        plant.image = data['image']
        plant.price = data['price']
        db.session.commit()
        return jsonify(plant.to_dict())
    
    def patch(self, plant_id):
        plant = Plant.query.get(plant_id)
        plant.update(**request.get_json())
        db.session.commit()
        return jsonify(plant.to_dict())
    
    def delete(self, plant_id):
        plant = Plant.query.get(plant_id)
        db.session.delete(plant)
        db.session.commit()
        return jsonify(plant.to_dict())
        
api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
