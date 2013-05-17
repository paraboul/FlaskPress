# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, make_response, request
from flaskpress import app
from flaskpress.settings import fp, theme
from flaskpress.models.pages import Page
from flaskpress.models.posts import Post, Category, Tag

@app.route('/')
@app.route('/index.html')
def default():
  fp['page'] = None
  page = Page.query.filter_by(link='index').first()
  if page:
    fp['page'] = page
    fp['title'] = page.title
    fp['breadcrumb'] = []
    
  return render_template(
    theme['active']+'/'+'home.html',
    fp=fp
  )

@app.route('/<slug>.html')
def single(slug):
  fp['page'] = None
  page = Page.query.filter_by(link=slug).first()
  if page:
    fp['page'] = page
    fp['title'] = page.title
    fp['breadcrumb'] = [
      {'v' : page.title}
    ]
  else:
    abort(404)
  return render_template(
    theme['active']+'/'+'page.html',
    fp=fp
  )

'''
  Robots
'''
@app.route('/robots.txt')
def robots():
  txt = "User-agent: *\nAllow: /\nSitemap: "+request.url_root+'sitemap.xml'
  response = make_response(txt)
  response.headers['Content-Type'] = 'text/plain; charset=utf-8'

  return response 

'''
  Sitemap
'''
@app.route('/sitemap.xml')
def sitemap():
  posts       = Post.query.order_by(Post.created.desc()).all()
  categories  = Category.query.all()
  pages       = Page.query.order_by(Page.created.desc()).all()
  tags        = Tag.query.all()

  response = make_response(
    render_template(
      'sitemap.xml', 
      url=request.url_root,
      posts=posts, 
      pages=pages,
      categories=categories,
      tags=tags
    )
  )

  response.headers['Content-Type'] = 'application/xml'

  return response
'''
  Errors
'''
@app.errorhandler(404)
def page_not_found(exception):
  return  render_template(
    '_404.html',
    fp=fp,
    exception=exception
  ), 404

@app.errorhandler(500)
def internal_error(exception):
  return  render_template(
    '_500.html',
    fp=fp,
    exception=exception
  ), 500

@app.errorhandler(400)
def internal_error(exception):
  return  render_template(
    '_400.html',
    fp=fp,
    exception=exception
  ), 400
