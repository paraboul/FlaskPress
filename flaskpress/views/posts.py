# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, make_response, abort, request
from flaskpress import app
from flaskpress.settings import fp, theme
from flaskpress.tools import get_page, remove_html_tags
from flaskpress.models.posts import Post, Category, Tag
from werkzeug.contrib.atom import AtomFeed

mod = Blueprint(
  'posts', 
  __name__, 
  url_prefix='/posts/'
)

'''
  posts
'''
@mod.route('/')
def list():
  posts = Post.query.order_by(Post.created.desc())
  posts = posts.paginate(get_page(), per_page=5)
  fp['posts'] = posts

  fp['breadcrumb'] = [
    {'v' : 'Articles'}
  ]

  fp['title'] = 'Posts'

  return render_template(
    theme['active']+'/'+'posts.html',
    fp=fp
  )

@mod.route('<slug>.html')
def single(slug):
  post = Post.query.filter_by(link=slug).first()

  if (post):
    fp['post'] = post

    fp['breadcrumb'] = [
      {'a' : '/posts/', 'v' : 'Articles'},
      {'v' : post.title}
    ]

    fp['title'] = post.title

    return render_template(
      theme['active']+'/'+'post.html',
      fp=fp
    )
  else:
    abort(404)

'''
  categories
'''
@mod.route('c/')
def categories():
  categories = Category.query.order_by(Category.title.asc()).all()
  fp['categories'] = categories

  fp['breadcrumb'] = [
    {'v' : 'Categories'}
  ]

  fp['title'] = 'Category'

  return render_template(
    theme['active']+'/'+'categories.html',
    fp=fp
  )


@mod.route('c/<slug>.html')
def category(slug):
  category = Category.query.filter_by(link=slug).first()
  if (category):
    posts = Post.query.filter_by(id_category=category.id).order_by(Post.created.desc())
    posts = posts.paginate(get_page(), per_page=5)
    fp['category'] = category
    fp['posts']    = posts

    fp['breadcrumb'] = [
      {'a' : '/posts/c/', 'v' : 'Categories'},
      {'v' : category.title}
    ]

    fp['title'] = category.title

    return render_template(
      theme['active']+'/'+'category.html',
      fp=fp
    )
  else:
    abort(404)

'''
  tags
'''
@mod.route('t/')
def tags():
  tags = Tag.query.order_by(Tag.name.asc()).all()
  fp['tags'] = tags
  fp['breadcrumb'] = [
    {'v' : 'Tags'}
  ]
  fp['title'] = 'Tags'

  return render_template(
    theme['active']+'/'+'tags.html',
    fp=fp
  )

@mod.route('t/<slug>.html')
def tag(slug):
  tag = Tag.query.filter_by(link=slug).first()
  if (tag):
    posts = Post.query.filter(Post.tags.contains(tag)).order_by(Post.created.desc())
    posts = posts.paginate(get_page(), per_page=5)
    fp['tag'] = tag
    fp['posts'] = posts

    fp['breadcrumb'] = [
      {'a' : '/posts/t/', 'v' : 'Tags'},
      {'v' : tag.name}
    ]

    fp['title'] = tag.name

    return render_template(
      theme['active']+'/'+'tag.html',
      fp=fp
    )
  else:
    abort(404)

'''
  feed
'''
@mod.route('feed.atom')
def feed():
  feed = AtomFeed(
    fp['site']['title'],
    feed_url=request.url_root+'posts/feed.atom/',
    url=request.url_root
  )

  posts = Post.query.filter_by().order_by(Post.created.desc()).limit(15).all()

  if (len(posts) == 0):
    return 'No feed.'

  for post in posts:
    feed.add(
      post.title, 
      unicode(remove_html_tags(post.body)),
      content_type='html',
      author=fp['site']['title'],
      url=request.url_root+'posts/'+post.link+'.html',
      updated=post.updated,
      published=post.created
    )

  return feed.get_response()
