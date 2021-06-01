
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login.utils import login_required

### custom imports
# Forms
from blog.users.forms import (
    RegistrationForm, LoginForm, UpdateAccountForm, 
    RequestResetForm, ResetPasswordForm
    )
# DB models
from blog import db
from blog.models import User, Post
# login manager
from flask_login import login_user, logout_user, current_user, login_required
# PasswordEncryption
from blog import bcrypt
# utils
from blog.users.utils import savePicture, sendResetMail



users = Blueprint('users',__name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You can now log in. - {user}', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Registration', form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Login unsuccessful! Please check login credentials', 'danger')
    return render_template('login.html', title='Log-In', form=form)


@users.route("/logout")
def logout():
    logout_user()
    flash(f'You have been logged out! See you soon!', 'info')
    return redirect(url_for('main.home'))


@users.route("/account", methods=["GET", "POST"])
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
        return redirect(url_for('users.account'))
    elif  request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file = url_for('static', filename=f'profile/{current_user.img_profile}')
    return render_template('account.html', image_file=image_file, 
                            title='THE Account', form=form)



@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', user=user, posts=posts, title='THE Blog')




@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        sendResetMail(user)
        flash('email sent', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', form=form, title='Forgot Password')


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verifyResetToken(token)
    if user is None:
        flash('invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been changed! You can now log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form=form, title='Reset Password')

