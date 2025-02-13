#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


@app.get("/restaurants")
def get_restaurants():
    restaurants = Restaurant.query.all()
    return {"restaurants": [restaurant.to_dict() for restaurant in restaurants]}, 200


@app.get("/restaurants/<int:id>")
def get_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    return {"restaurant": restaurant.to_dict()}, 200

@app.delete("/restaurants/<int:id>")
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()
    return make_response("", 204)

@app.get("/pizzas")
def get_pizzas():
    pizzas = Pizza.query.all()
    return {"pizzas": [pizza.to_dict() for pizza in pizzas]}, 200   

@app.post("/restaurantpizzas")
def create_restaurant_pizza():
    data = request.json
    restaurant_id = data.get("restaurant_id")
    pizza_id = data.get("pizza_id")
    price = data.get("price")

    restaurant = Restaurant.query.get_or_404(restaurant_id)
    pizza = Pizza.query.get_or_404(pizza_id)

    restaurant_pizza = RestaurantPizza(restaurant_id=restaurant_id, pizza_id=pizza_id, price=price)
    db.session.add(restaurant_pizza)
    db.session.commit()

    return {"restaurant_pizza": restaurant_pizza.to_dict()}, 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
