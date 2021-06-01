
from flask import Blueprint, render_template, request

### custom imports
# Forms
# DB models
from blog.models import Post


main = Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
@main.route("/blog")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # posts = Post.query.order_by(Post.date_posted.desc())
    # posts = Post.query.order_by(Post.date_posted.desc).all()
    return render_template('home.html', posts=posts, title='THE Blog')

@main.route("/about")
def about():
    return render_template('about.html')


@main.route("/hello")
def greet():
    return f'<h1> Hello there!<h1></br><h1> General Kenobi!<h1></br>'