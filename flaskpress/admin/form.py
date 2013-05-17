# -*- coding: utf-8 -*-
from flask import current_app
from flask.ext.wtf import Form, TextField, Required, QuerySelectField, PasswordField, SelectMultipleField, SelectField, TextAreaField
from flask.ext.principal import Identity, identity_changed
from flaskpress.models.users import User
from flaskpress.models.posts import Category
from flaskpress.models.pages import Page
from flaskpress.tools import slugify
from flaskpress import app

'''
  Login
'''
class LoginForm(Form):
  email    = TextField('E-Mail', validators=[Required()])
  password = PasswordField('Password', validators=[Required()])

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
    self.user = None

  def validate(self):
    rv = Form.validate(self)
    if not rv:
      return False

    user = User.query.filter_by(email=self.email.data).first()
    if user is None:
      self.email.errors.append(u'Unknown e-mail.')
      return False

    if not user.check_password(self.password.data):
      self.password.errors.append(u'Invalid password.')
      return False

    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
    self.user = user
    return True

'''
  Categories
'''
class CategoryForm(Form):
  title   = TextField(u'Title', validators=[Required()])
  body    = TextAreaField(u'Description', validators=[Required()])
  link    = TextField(u'Slug', validators=[Required()])

class CategoryMultiForm(Form):
  actions  = SelectField(u'Actions', choices=[('D', 'Delete')])

'''
  Posts
'''
class PostForm(Form):
  title        = TextField(u'Title', validators=[Required()])
  body         = TextAreaField(u'Content', validators=[Required()])
  tags         = TextField(u'Tags', validators=[Required()])
  link         = TextField(u'Permalink', validators=[Required()])
  id_category  = QuerySelectField(
    allow_blank=True, 
    get_label=lambda x: str(x.title), 
    query_factory=lambda: Category.query.order_by('title'),
    blank_text=u'-- Category ---'
  )

class PostMultiForm(Form):
  actions  = SelectField(u'Actions', choices=[('D', 'Delete')])


'''
  Pages
'''
class PageForm(Form):
  title     = TextField(u'Title', validators=[Required()])
  link      = TextField(u'Permalink', validators=[Required()])
  body      = TextAreaField(u'Content', validators=[Required()])
  id_parent = QuerySelectField(
    allow_blank=True, 
    get_label=lambda x: str(x.title), 
    query_factory=lambda: Page.query.filter_by(id_parent=None).order_by('title'),
    blank_text=u'-- Parent ---'
  )

class PageMultiForm(Form):
  actions  = SelectField(u'Actions', choices=[('D', 'Delete')])
