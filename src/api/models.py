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


class FileUpload(db.Model):
    __tablename__ = "todo_user"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), unique=True, nullable=False)
    mimetype = db.Column(db.String(256), nullable=False)
    data = db.Column(db.LargeBinary)
