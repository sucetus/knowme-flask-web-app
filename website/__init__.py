from flask import Flask, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os

current_dir = os.path.dirname("static")


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'TREASUREHUNTR'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
    # postgres://knowme_postgresql_user:6jp6v2hGpJD3VFlv9OgrgyjugDnnzwcG@dpg-ch8n151jvhtqmk2bpo70-a.oregon-postgres.render.com/knowme_postgresql
    db.init_app(app)

    with app.app_context():
        from .views import views
        from .auth import auth

        app.register_blueprint(views, url_prefix = '/')
        app.register_blueprint(auth, url_prefix = '/')

        create_database(app)

        from .models import User, Stats

        login_manager = LoginManager()
        login_manager.login_view = "auth.login"
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(id):
            return User.query.get(int(id))

    return app


def create_database(app):
    with app.app_context():
        if not path.exists('website' + DB_NAME):
            db.create_all()
            print('Database Created')