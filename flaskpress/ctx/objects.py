from flaskpress import app
from flaskpress.models.pages import Page
from flaskpress.models.posts import Post, Category, Tag

@app.context_processor
def init_objects():
  return dict(
    fpLastPost=Post.query.order_by(Post.created.desc()).first(),
    fpLastPosts=Post.query.order_by(Post.created.desc()).limit(5).all(),
    fpCategories=Category.query.order_by(Category.title.asc()).all()
  )
