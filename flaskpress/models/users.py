# -*- coding: utf-8 -*-
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flaskpress import app, db, lg
from flaskpress.tools import generate_password

from datetime import datetime

roles_users = db.Table(
  'roles_users',
  db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
  db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
  id            = db.Column(db.Integer(), primary_key=True)
  name          = db.Column(db.String(80), unique=True)
  description   = db.Column(db.String(255))

class User(db.Model, UserMixin):
  id            = db.Column(db.Integer, primary_key = True)
  created       = db.Column(db.Date, default=datetime.today())
  email         = db.Column(db.String(120), unique=True, index=True)
  firstname     = db.Column(db.String(80))
  lastname      = db.Column(db.String(80))
  password      = db.Column(db.String(40), default=generate_password())
  active        = db.Column(db.Boolean())
  confirmed_at  = db.Column(db.DateTime(), default=datetime.today())
  roles         = db.relationship('Role', secondary=roles_users, backref=db.backref('user', lazy='dynamic'))

  def __repr__(self):
    return '<User %r>' % (self.email)

  def check_password(self, pwd):
    if self.password == pwd:
      return True
    return False

  def is_authenticated(self):
    return True

  def is_active(self):
    return self.active

  def is_anonymous(self):
    return False

  def get_id(self):
    return unicode(self.id)

  def create_user(self):
    return None

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@lg.user_loader
def load_user(id):
  return User.query.filter_by(id=int(id)).first()
