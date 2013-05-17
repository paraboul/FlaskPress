# -*- coding: utf-8 -*-
from flaskpress import app, db
from datetime import datetime

tags_posts = db.Table(
  'tags_posts', 
  db.Column('post_id', 
    db.Integer(), 
    db.ForeignKey('post.id')
  ),
  db.Column(
    'tag_id', 
    db.Integer(), 
    db.ForeignKey('tag.id')
  )
)

class Tag(db.Model): 
  id    = db.Column(db.Integer(), primary_key=True)
  name  = db.Column(db.String(80), unique=True)
  link  = db.Column(db.String(80), unique=True)
  posts = db.relationship('Post', secondary=tags_posts, backref=db.backref('post', lazy='dynamic'))

  def __repr__(self):
    return '%s' % self.name

class Post(db.Model):
  id            = db.Column(db.Integer, primary_key = True)
  id_category   = db.Column(db.Integer, db.ForeignKey('category.id'))
  category      = db.relationship('Category', backref=db.backref('category'))

  link    = db.Column(db.String(200), unique=True)
  created = db.Column(db.Date, default=datetime.utcnow())
  updated = db.Column(db.Date, default=datetime.utcnow())
  title   = db.Column(db.String(200))
  body    = db.Column(db.Text())
  tags    = db.relationship('Tag', secondary=tags_posts, backref=db.backref('tag', lazy='dynamic'))

  tagsTxt = property(lambda s: ','.join(map(str, s.tags)))

  def __repr__(self):
    return '<Post #%s>' % self.title

class Category(db.Model):
  id      = db.Column(db.Integer, primary_key = True)
  title   = db.Column(db.String(200))
  link    = db.Column(db.String(200), unique=True)
  body    = db.Column(db.Text())

  posts = property(lambda s: Post.query.filter_by(id_category=s.id).count()) 

  def __repr__(self):
    return '<Category #%s>' % self.title