# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from werkzeug.contrib.fixers import ProxyFix

from flaskpress.settings import theme
from flaskpress.config import Config
from flaskpress.tools import ModifiedLoader

# Init Flask
app = Flask(
  __name__, 
  template_folder='themes/', 
  static_folder='themes/'+theme['active']+'/static/',
  static_url_path='/static'
)
app.config.from_object(Config)

app.wsgi_app = ProxyFix(app.wsgi_app)
db = SQLAlchemy(app)
lg = LoginManager()
lg.setup_app(app)

Bootstrap(app)

# Blueprints & shit
from flaskpress.ctx import objects, filters
from flaskpress.models import users
from flaskpress.views  import default

from flaskpress.views.pages import mod as pages_bp
from flaskpress.views.posts import mod as posts_bp
from flaskpress.admin.view  import mod as admin_bp

# Blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(pages_bp)
app.register_blueprint(posts_bp)

# Tpls
app.jinja_options = Flask.jinja_options.copy() 
app.jinja_options['loader'] = ModifiedLoader(app)
