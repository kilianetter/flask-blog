
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort 
from flask_login import current_user, login_required

### custom imports
# Forms
from blog.posts.forms import CreatePostForm
# DB models
from blog import db
from blog.models import Post


posts = Blueprint('posts',__name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        flash('Your post has been created', 'success')
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', 
                            form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title= post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
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


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted', 'success')
    return redirect(url_for('main.home'))