from flask.ext.script import Manager
from flaskpress.settings import admin
from flaskpress.models.users import User, Role, user_datastore
from flaskpress.models import pages, posts
from flaskpress import app, db

manager = Manager(app)

@manager.command
def init_db():
  print 'Initialising database'

  db.create_all()

@manager.command
def drop_db():
  print 'Dropping database'

  db.drop_all()

@manager.command
def init():
  drop_db()
  init_db()
  init_roles()
  init_categories()
  init_admin()

@manager.command
def init_roles():
  print 'Initialising roles'

  roles = [
    ['admin','Administrator'],
    ['author','Author'],
    ['user','User']
  ]

  for title, body in roles:
    r = Role(name=title, description=body)
    db.session.add(r)

  db.session.commit()

@manager.command
def init_admin():
  print 'Initialising admin'

  user_datastore.create_user(
    firstname=admin['firstname'], 
    lastname=admin['lastname'], 
    email=admin['email'], 
    password=admin['password']
  )

  db.session.commit()

  user = User.query.filter_by(email=admin['email']).first()
  user_datastore.add_role_to_user(user, 'admin')
  user_datastore.add_role_to_user(user, 'author')
  user_datastore.add_role_to_user(user, 'user')

  db.session.commit()

@manager.command
def init_categories():
  print 'Initialising categories'
  category = posts.Category()
  category.title  = 'Posts'
  category.link   = 'posts'
  category.body  = 'Posts'

  db.session.add(category)
  db.session.commit()

if __name__ == '__main__':
  manager.run()
