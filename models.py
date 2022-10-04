"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.Text, server_default= 'https://everydaynutrition.co.uk/wp-content/uploads/2015/01/default-user-avatar.png')


    def __repr__(self):
        return f'<User id = {self.id} first_name = {self.first_name} last_name = {self.last_name} image_url = {self.image_url}'