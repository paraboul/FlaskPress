# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from flask import current_app, flash, redirect, session
from flask.ext.login import current_user
from flask.ext.security import roles_required, roles_accepted
from flask.ext.login import login_user, logout_user
from flaskpress import app, db
from flaskpress.settings import fp
from flaskpress.tools import slugify_unique, slugify
from flaskpress.admin.form import LoginForm
from flaskpress.admin.form import CategoryForm, CategoryMultiForm
from flaskpress.admin.form import PostForm, PostMultiForm
from flaskpress.admin.form import PageForm, PageMultiForm
from flaskpress.models.posts import Category, Post, Tag
from flaskpress.models.pages import Page
import string

mod = Blueprint(
  'admin', 
  __name__, 
  url_prefix='/admin',
  template_folder='templates/', 
  static_folder='static/',
  static_url_path='/static'
)

'''
  Default views
'''
@mod.url_value_preprocessor
def fill_fp(endpoint, values):
  fp['user'] = current_user
  fp['page'] = endpoint.replace('admin.', '')

@mod.route('/')
@roles_required('admin')
def home():
  fp['breadcrumb'] = [{'v' : 'Home'}]

  return render_template(
    'admin_home.html',
    fp=fp
  )


'''
  Admin - Categories
'''
@mod.route('/categories/', methods=['GET', 'POST'])
def categories():
  fp['breadcrumb'] = [{'v' : 'Categories'}]
  categories = Category.query.all()
  categoryForm  = CategoryForm()
  categoryMultiForm = CategoryMultiForm(prefix="multi_")
  
  if request.args.get('q') == 'add' and categoryForm.validate_on_submit():
    category = Category()
    categoryForm.populate_obj(category)
    category.link = slugify_unique(category.link, Category)
    db.session.add(category)
    db.session.commit()
    return redirect('/admin/categories/')

  if request.args.get('q') == 'multi':
    if request.form['multi_actions'] == 'D':
      ids = request.form.getlist('selected')
      for id in ids:
        to_del = Category.query.filter_by(id=id).first()
        db.session.delete(to_del)

      db.session.commit()

    return redirect('/admin/categories/')

  return render_template(
    'admin_categories.html',
    fp=fp,
    categories=categories,
    categoryForm=categoryForm,
    categoryMultiForm=categoryMultiForm
  )

@mod.route('/categories/<int:id>/', methods=['GET', 'POST'])
def category_id(id):
  try:
    category = Category.query.filter_by(id=id).first()
    categoryForm  = CategoryForm(obj=category)
  except:
    redirect('/admin/categories/')

  if categoryForm.validate_on_submit():
    prevCategory = category
    categoryForm.populate_obj(category)
    category.link = slugify_unique(category.link, Category, prevCategory)

    db.session.commit()
    return redirect('/admin/categories/')

  fp['breadcrumb'] = [
    {'a' : '/admin/categories/', 'v' : 'Categories'},
    {'v' : category.title}
  ]

  return render_template(
    'admin_category.html',
    fp=fp,
    category=category,
    categoryForm=categoryForm
  )

'''
  Admin - Posts
'''
@mod.route('/posts/', methods=['GET', 'POST'])
def posts():
  fp['breadcrumb'] = [{'v' : 'Posts'}]
  posts = Post.query.all()
  postForm  = PostForm()
  postMultiForm = PostMultiForm(prefix="multi_")

  if request.args.get('q') == 'add' and postForm.validate_on_submit():
    post = Post(
      id_category = postForm.data['id_category'].id,
      link        = postForm.data['link'],
      title       = postForm.data['title'],
      body        = postForm.data['body']
    )
    tags = string.split(postForm.data['tags'], ',')
    post.link = slugify_unique(post.link, Post)
    db.session.add(post)
    db.session.commit()

    for tag in tags:
      try:
        existing = Tag.query.filter_by(link=slugify(tag)).one()
        post.tags.append(existing)
      except:
        new_tag = Tag(name=tag, link=slugify(tag))
        db.session.add(new_tag)
        db.session.commit()
        post.tags.append(new_tag)
        
    db.session.commit()

    return redirect('/admin/posts/')

  if request.args.get('q') == 'multi':
    if request.form['multi_actions'] == 'D':
      ids = request.form.getlist('selected')
      for id in ids:
        to_del = Post.query.filter_by(id=id).first()
        db.session.delete(to_del)

      db.session.commit()

    return redirect('/admin/posts/')

  return render_template(
    'admin_posts.html',
    fp=fp,
    posts=posts,
    postForm=postForm,
    postMultiForm=postMultiForm
  )

@mod.route('/posts/<int:id>/', methods=['GET', 'POST'])
def post_id(id):
  try:
    post = Post.query.filter_by(id=id).first()
    postForm  = PostForm(obj=post)
  except:
    return redirect('/admin/posts/')

  if postForm.validate_on_submit():
    post.link = slugify_unique(postForm.data['link'], Post, post)
    post.title       = postForm.data['title']
    post.body        = postForm.data['body']

    if postForm.data['id_category']:
      post.id_category = postForm.data['id_category'].id
    else:
      post.id_category = None

    for tag in post.tags:
      post.tags.remove(tag)

    db.session.commit()

    tags = string.split(postForm.data['tags'], ',')
    for tag in tags:
      try:
        existing = Tag.query.filter_by(link=slugify(tag)).one()
        post.tags.append(existing)
      except:
        new_tag = Tag(name=tag, link=slugify(tag))
        db.session.add(new_tag)
        db.session.commit()
        post.tags.append(new_tag)
        
    db.session.commit()
    return redirect('/admin/posts/'+str(id)+'/')
  else:
    postForm.tags.data = post.tagsTxt
    postForm.id_category.data = post.category

  fp['breadcrumb'] = [
    {'a' : '/admin/posts/', 'v' : 'Posts'},
    {'v' : post.title}
  ]

  return render_template(
    'admin_post.html',
    fp=fp,
    post=post,
    postForm=postForm
  )

@mod.route('/pages/', methods=['GET', 'POST'])
def pages():
  fp['breadcrumb'] = [{'v' : 'Pages'}]
  pages = Page.query.filter_by(id_parent=None).all()
  pageForm  = PageForm()
  pageMultiForm = PageMultiForm(prefix="multi_")

  if request.args.get('q') == 'add' and pageForm.validate_on_submit():
    page = Page()
    pageForm.populate_obj(page)

    if pageForm.data['id_parent']:
      page.id_parent = pageForm.data['id_parent'].id

    page.link = slugify_unique(page.link, Page)
    db.session.add(page)
    db.session.commit()
      
    return redirect('/admin/pages/')

  if request.args.get('q') == 'multi':
    if request.form['multi_actions'] == 'D':
      ids = request.form.getlist('selected')
      for id in ids:
        to_del = Page.query.filter_by(id=id).first()
        db.session.delete(to_del)

      db.session.commit()

    return redirect('/admin/pages/')

  return render_template(
    'admin_pages.html',
    fp=fp,
    pages=pages,
    pageForm=pageForm,
    pageMultiForm=pageMultiForm
  )

@mod.route('/pages/<int:id>/', methods=['GET', 'POST'])
def page_id(id):
  try:
    page = Page.query.filter_by(id=id).first()
    pageForm  = PageForm(obj=page)
  except:
    return redirect('/admin/pages/')

  if pageForm.validate_on_submit():
    page.link = slugify_unique(pageForm.data['link'], Page, page)
    page.title       = pageForm.data['title']
    page.body        = pageForm.data['body']

    if pageForm.data['id_parent']:
      page.id_parent = pageForm.data['id_parent'].id
    else:
      page.id_parent = None

    db.session.commit()
    return redirect('/admin/pages/'+str(id)+'/')
  else:
    pageForm.id_parent.data = page.parent

  fp['breadcrumb'] = [
    {'a' : '/admin/pages/', 'v' : 'Pages'},
    {'v' : page.title}
  ]

  return render_template(
    'admin_page.html',
    fp=fp,
    page=page,
    pageForm=pageForm
  )


@mod.route('/options/')
def options():
  return 'options'

'''
  User: Login & logout
'''
@mod.route('/login/', methods=['GET', 'POST'])
def login():
  fp['breadcrumb'] = [{'v' : 'Login'}]

  form = LoginForm()
  if form.validate_on_submit():
    login_user(form.user, True)
    flash(u'Logged in successfully.', 'success')

    return redirect('/admin/')

  return render_template(
    'admin_login.html',
    fp=fp,
    user_login=form
  )

@mod.route('/logout/')
def logout():
  logout_user()
  for key in ('identity.name', 'identity.auth_type'):
    session.pop(key, None)
  
  flash(u'Logged out successfully.', 'success')
  return redirect('/admin/')