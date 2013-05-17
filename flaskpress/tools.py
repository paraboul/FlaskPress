# -*- coding: utf-8 -*-
from flask import request
from flask.templating import DispatchingJinjaLoader
from flask.globals import _request_ctx_stack
from sqlalchemy.sql import and_
from unidecode import unidecode
import string, random, re

class ModifiedLoader(DispatchingJinjaLoader):
  def _iter_loaders(self, template):
    bp = _request_ctx_stack.top.request.blueprint
    if bp is not None and bp in self.app.blueprints:
      loader = self.app.blueprints[bp].jinja_loader
      if loader is not None:
        yield loader, template

    loader = self.app.jinja_loader
    if loader is not None:
      yield loader, template

def slugify(text, delim=u'-'):
  _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

  """Generates an ASCII-only slug."""
  result = []
  for word in _punct_re.split(text.lower()):
      result.extend(unidecode(word).split())
  return unicode(delim.join(result))

def slugify_unique(slug, Obj, current=False):
  id   = 0

  if current:
    id = current.id

  link = slugify(slug)

  count = Obj.query.filter(and_(Obj.link.like(link+'%'), Obj.id != id)).count()

  while Obj.query.filter(and_(Obj.id != id), Obj.link == link).count() != 0:
    link = "%s-%d" % (link, count)
    count += 1 

  return link

def generate_password():
  char_set  = string.ascii_uppercase + string.digits
  return ''.join(random.sample(char_set, 6))

def get_page():
  if (request.args.get('page') is not None):
    page = int(request.args.get('page'))
  else:
    page = 1

  return page

def remove_html_tags(data):
  p = re.compile(r'<.*?>')
  return p.sub('', data) 