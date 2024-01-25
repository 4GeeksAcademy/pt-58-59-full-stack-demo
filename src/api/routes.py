"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import (
    db, User, TodoList, TodoItem
)
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# User views


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


# TodoList

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


# TodoItem

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
