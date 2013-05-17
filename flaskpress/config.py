# -*- coding: utf-8 -*-
from flaskpress.settings import config, theme

class Config(object):
  # SQLAlchemy
  SQLALCHEMY_DATABASE_URI = config['sql']

  # Debug
  DEBUG           = config['debug']
  TESTING         = config['testing']

  # Theme
  THEME           = theme['active']

  # Security
  SECURITY_UNAUTHORIZED_VIEW = '/admin/login/'
  SECRET_KEY = config['key']
