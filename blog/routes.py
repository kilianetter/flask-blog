from flask import render_template, url_for, flash, redirect, request, abort
from flask_login.utils import login_required
from flask_wtf import form


### custom imports
# App
from blog import app, db, bcrypt, mail
# Forms
from blog.forms import (
    RegistrationForm, LoginForm, UpdateAccountForm, 
    CreatePostForm, 
    RequestResetForm, ResetPasswordForm
    )
# DB models
from blog.models import User, Post
# login manager
from flask_login import login_user, logout_user, current_user, login_required
# mail
from flask_mail import Message

# secrets for picture upload -- why?
import secrets
import os
# image resizing
from PIL import Image


# Provide routes with Pages to render
@app.route("/")
@app.route("/home")
@app.route("/blog")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # posts = Post.query.order_by(Post.date_posted.desc())
    # posts = Post.query.order_by(Post.date_posted.desc).all()
    return render_template('home.html', posts=posts, title='THE Blog')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You can now log in. - {user}', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful! Please check login credentials', 'danger')
    return render_template('login.html', title='Log-In', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash(f'You have been logged out! See you soon!', 'info')
    return redirect(url_for('home'))


def savePicture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/profile', picture_fn)
    # image resizing
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            pictureFile = savePicture(form.picture.data)
            current_user.img_profile = pictureFile       
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif  request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file = url_for('static', filename=f'profile/{current_user.img_profile}')
    return render_template('account.html', image_file=image_file, 
                            title='THE Account', form=form)


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        flash('Your post has been created', 'success')
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', 
                            form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title= post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = CreatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been updated', 'success')
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='update post', post=post, 
                            form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', user=user, posts=posts, title='THE Blog')


def sendResetMail(user):
    token = user.getResetToken()
    msg = Message(
        'Password Reset Request', 
        sender="noreply@phobox.de",
        recipients=[user.email])
    msg.body = f'''
    To reset your password visit the following Link:
    {url_for('reset_token', token=token, _external=True)}
    if you did not make this requst, simply ignore this email. no changes have been made
    '''
    mail.send(msg)

@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        sendResetMail(user)
        flash('email sent', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', form=form, title='Forgot Password')


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verifyResetToken(token)
    if user is None:
        flash('invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been changed! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form, title='Reset Password')



@app.route("/hello")
def greet():
    return f'<h1> Hello there!<h1></br><h1> General Kenobi!<h1></br>'




