#! /usr/bin/env python3

from flask import Flask
from flask_socketio import SocketIO
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

webapp = Flask(__name__)
webapp.config.from_object(Config)
db = SQLAlchemy(webapp)
migrate = Migrate(webapp, db)
login = LoginManager(webapp)
bootstrap = Bootstrap(webapp)
socketio = SocketIO(webapp)

from webapp import routes, models

login.login_view = 'login'
