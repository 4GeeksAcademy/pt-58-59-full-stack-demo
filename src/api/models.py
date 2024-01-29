from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import (
    generate_password_hash, check_password_hash
)

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "todo_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(120), unique=True, nullable=False
    )
    _password = db.Column(
        db.String(256), unique=False, nullable=False
    )
    # todo_lists: List[TodoList]
    # todo_item: List[TodoItem]

    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password_hash(self, other):
        return check_password_hash(self._password, other)

    def __repr__(self):
        return f'<User {self.username}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
        }


todo_list_to_todo_item = db.Table(
    "todo_list_to_todo_item",
    db.metadata,
    db.Column(
        "todo_list_id",
        db.Integer,
        db.ForeignKey('todo_list.id')
    ),
    db.Column(
        "todo_item_id",
        db.Integer,
        db.ForeignKey('todo_item.id')
    ),
)


class TodoList(db.Model):
    __tablename__ = "todo_list"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, default="A really cool todo list!")
    user_id = db.Column(
        db.Integer, db.ForeignKey("todo_user.id")
    )
    user = db.relationship(
        "User",
        uselist=False,
        backref=db.backref(
            "todo_lists",
            uselist=True,
        )
    )
    todo_items = db.relationship(
        "TodoItem",
        secondary=todo_list_to_todo_item,
        primaryjoin=(id == todo_list_to_todo_item.c.todo_list_id),
        # secondaryjoin=(),
        uselist=True,
        backref=db.backref(
            "todo_lists",
            uselist=True
        )
    )

    def __repr__(self):
        return f'<TodoList {self.title}>'

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "user": self.user.serialize(),
            "todo_items": [{
                "id": todo.id,
                "label": todo.label,
                "done": todo.done,
                "created": todo.created,
                "updated": todo.updated,
            } for todo in self.todo_items],
        }


class TodoItem(db.Model):
    __tablename__ = "todo_item"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String, default="Some new thing to do.")
    done = db.Column(db.Boolean)
    created = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.now)
    user_id = db.Column(
        db.Integer, db.ForeignKey("todo_user.id")
    )
    user = db.relationship(
        "User",
        uselist=False,
        backref=db.backref(
            "todo_items",
            uselist=True,
        )
    )
    # todo_lists: List[TodoList]

    def __repr__(self):
        return f'<TodoItem {self.label}>'

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.serialize(),
            "label": self.label,
            "done": self.done,
            "created": self.created,
            "updated": self.updated,
            "todo_lists": [{
                "id": todo_list.id,
                "title": todo_list.title,
            } for todo_list in self.todo_lists],
        }
