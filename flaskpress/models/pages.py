# -*- coding: utf-8 -*-
from flaskpress import app, db
from datetime import datetime

class Page(db.Model):
  id        = db.Column(db.Integer, primary_key=True)
  title     = db.Column(db.Text, unique=True)
  link      = db.Column(db.Text, unique=True)
  body      = db.Column(db.Text)
  type      = db.Column(db.Text)
  created   = db.Column(db.Date, default=datetime.utcnow())
  updated   = db.Column(db.Date, default=datetime.utcnow())

  childs    = property(lambda s: s.query.filter_by(id_parent=s.id).all()) 

  def __repr__(self):
    return '<Page #%r>' % self.id

Page.id_parent = db.Column(db.Integer, db.ForeignKey('page.id'))
Page.parent    = db.relationship('Page', backref=db.backref('page'), remote_side=Page.id)
