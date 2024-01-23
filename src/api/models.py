from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "todo_user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    # todo_lists: List[TodoList]
    # todo_item: List[TodoItem]

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
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
        uselist=True
    )

    

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
    todo_lists = db.relationship(
        "TodoList",
        secondary=todo_list_to_todo_item,
        primaryjoin=(id == todo_list_to_todo_item.c.todo_item_id),
        uselist=True
    )

