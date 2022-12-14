"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False, unique=True)
    last_name = db.Column(db.String(20), nullable=False, unique=True)
    image_url = db.Column(db.Text, server_default= 'https://everydaynutrition.co.uk/wp-content/uploads/2015/01/default-user-avatar.png')


    def __repr__(self):
        return f'<User id = {self.id} first_name = {self.first_name} last_name = {self.last_name} image_url = {self.image_url}'

class Post(db.Model):
    """User posts."""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='posts')
    # Create a through relationship
    tags = db.relationship('Tag', secondary='post_tag', backref='posts' )

class Tag(db.Model):
    """Categories for each post"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.Text, nullable=False, unique=True)

class PostTag(db.Model):
    """Which tags are associated with each user post."""
    __tablename__ = 'post_tag'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
