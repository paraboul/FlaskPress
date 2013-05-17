# -*- coding: utf-8 -*-
from flask import Blueprint
from flaskpress import app

mod = Blueprint(
  'pages', 
  __name__, 
  url_prefix='/pages/'
)
