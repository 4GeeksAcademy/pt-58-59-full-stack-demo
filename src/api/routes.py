"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import re

from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import (
    create_access_token, get_jwt_identity, jwt_required,
    current_user
)
import requests

from api.models import (
    db, User, TodoList, TodoItem
)
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# region: Auth

@api.route("/token", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(
        username=data.get("username", None)
    ).first()

    if user is None:
        return jsonify(
            message="Invalid credentials",
        ), 400
    
    if not user.check_password_hash(data.get("password", "")):
        return jsonify(
            message="Invalid credentials",
        ), 400
    
    return jsonify(
        access_token=create_access_token(
            identity=user.username
        ),
        token_type="bearer",
    )


@api.route("/authtest", methods=["GET"])
@jwt_required()
def auth_test():
    return jsonify(current_user.serialize())

# endregion

# region: User views

@api.route("/user", methods=["GET"])
def read_users():
    users = User.query.all()
    return jsonify(
        users=[user.serialize() for user in users]
    )


@api.route("/user/<int:id>", methods=["GET"])
def read_user(id: int):
    user = User.query.filter_by(id=id).first()
    return jsonify(user.serialize())


@api.route("/user", methods=["POST"])
def create_user():
    """
    BODY:
    {
        "username": "string",
        "password": "string"
    }
    """
    data = request.json
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    return jsonify(user.serialize()), 201


# endregion

# region: TodoList

@api.route("/todolist", methods=["POST"])
def create_todo_lists():
    data = request.json
    db_user = User.query.filter_by(
        email=data.get("user", "Ooops?")
    ).first()
    todo_list = TodoList(
        title=data.get("title", "DEFAULT TITLE"),
        user=db_user
    )
    db.session.add(todo_list)
    db.session.commit()
    db.session.refresh(todo_list)
    return jsonify(todo_list.serialize())


@api.route("/todolist", methods=["GET"])
def read_todo_lists():
    todo_lists = TodoList.query.all()
    return jsonify(
        todo_lists=[todo_list.serialize() for todo_list in todo_lists]
    )


@api.route("/todolist/<int:id>", methods=["GET"])
def read_todo_list(id: int):
    todo_list = TodoList.query.filter_by(id=id).first()
    return jsonify(todo_list.serialize())


@api.route("/todolist/<int:id>", methods=["PUT"])
def update_todo_list(id: int):
    data = request.json
    todo_list = TodoList.query.filter_by(id=id).first()
    if not todo_list:
        return jsonify(message="Todo list not found!"), 404
    for k, v in data.items():
        setattr(todo_list, k, v)
    db.session.merge(todo_list)
    db.session.commit()
    db.session.refresh(todo_list)
    return jsonify(todo_list.serialize())


@api.route("/todolist/<int:id>", methods=["DELETE"])
def delete_todo_list(id: int):
    todo_list = TodoList.query.filter_by(id=id).first()
    if not todo_list:
        return jsonify(message="Todo list not found!"), 404
    db.session.delete(todo_list)
    db.session.commit()
    return "", 204

# endregion

# region: TodoItem

@api.route("/todoitem", methods=["POST"])
def create_todo_item():
    pass


@api.route("/todoitem", methods=["GET"])
def read_todo_items():
    todo_items = TodoItem.query.all()
    return jsonify(
        todo_items=[todo_item.serialize() for todo_item in todo_items]
    )


@api.route("/todoitem/<int:id>", methods=["GET"])
def read_todo_item(id: int):
    todo_item = TodoItem.query.filter_by(id=id).first()
    return jsonify(todo_item.serialize())


@api.route("/todoitem", methods=["PUT"])
def update_todo_item():
    pass


@api.route("/todoitem", methods=["DELETE"])
def delete_todo_item():
    pass

# endregion

# region: Spoonacular

@api.route("/recipes/search", methods=["GET"])
def search_recipes():
    params = dict(request.args)
    params["apiKey"] = os.getenv("SPOON_API_KEY")
    url = "https://api.spoonacular.com/recipes/complexSearch"
    resp = requests.get(url, params=params)
    return jsonify(resp.json()), resp.status_code


@api.route("/recipes/parse", methods=["POST"])
def parse_recipes():
    params = dict(request.args)
    params["apiKey"] = os.getenv("SPOON_API_KEY")
    url = "https://api.spoonacular.com/recipes/analyzeInstructions"
    resp = requests.post(url, params=params)
    return jsonify(resp.json()), resp.status_code

# endregion

"""
Cook short pasta and drain off the water, leaving 1/4 cup of reserved pasta water.  Put the pasta back in the pot, melt in 1 tbs of butter, add in 1.5 tsp of mustard powder, 1/2 tsp of ground black pepper, a pinch of salt, your reserved pasta water, 1/4 c grated cheese, stir until the cheese is melted and incorporated.  Add milk as needed to get the right consistency.
"""
