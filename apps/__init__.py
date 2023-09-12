# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from datetime import datetime
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module


db = SQLAlchemy()
login_manager = LoginManager()

def make_shell_context(app):

    from apps.authentication.models import Users
    from apps.home.models import Bill

    @app.shell_context_processor
    def add_shell_context():
        user1 = Users()
        user1.username = 'admin'
        user2 = Users()
        user2.username = 'user'
        user3 = Users()
        user3.username = 'superuser'   
        bill = Bill()
        bill.id = 0
        bill.value = 150.0
        bill.timestamp = datetime.utcnow()
        bill.payed_by = user1.id
        return {'db': db,'users': Users, 'bill': Bill, 'admin': user1,'testbill': bill}

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print('> Fallback to SQLite ')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

from apps.authentication.oauth import github_blueprint

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    app.register_blueprint(github_blueprint, url_prefix="/login")    
    configure_database(app)
    make_shell_context(app)
    return app
