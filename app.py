"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app) # WANT TO HAVE URI ALREADY CONFIGURED URI BEFORE THIS 

@app.route('/')
def show_nothing():
    return redirect('/users')

@app.route('/users')
def show_all_users():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/users/<user_id>')
def show_user_details(user_id):
    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template('user_details.html', user=user, posts=posts)

@app.route('/users/new')
def show_add_user_form():
    return render_template('new_user_form.html')

@app.route('/users/new', methods=["POST"])
def add_new_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image = request.form["image"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users') 

@app.route('/users/<user_id>/edit')
def show_user_edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user_form.html', user=user)

@app.route('/users/<user_id>/edit', methods=["POST"])
def update_user(user_id):
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image = request.form["image"]

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image

    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<user_id>/posts/new')
def show_new_post_form(user_id):
    user = User.query.get(user_id) 
    return render_template('add_post_form.html', user=user)

@app.route('/users/<user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    title = request.form["title"]
    content = request.form["content"]

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('show_post.html', post=post)

@app.route('/posts/<post_id>/edit')
def show_edit_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<post_id>/edit', methods=["POST"])
def edit_post(post_id):
    new_title = request.form["title_edit"]
    new_content = request.form["content_edit"]
    post = Post.query.get_or_404(post_id)
    post.title = new_title
    post.content = new_content
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.user
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{user.id}')
    # delete post from db
    # redirect to 