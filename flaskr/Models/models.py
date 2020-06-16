from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate
import os

db = SQLAlchemy()


def app_config(app):
    # Setting up Database & app config

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('PROJECT_SECRET')
    db.app = app
    db.init_app(app)
    # Setting up Migration
    Migrate(app, db)

    db.create_all()


# MODELS: TABLES

class Users(db.Model, UserMixin):
    """
    User's Table
    """
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, email, password):
        self.email = email
        self.username = username
        self.password = password

    def display(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()
