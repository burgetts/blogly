# Seed user, post, tags, post_tag
from models import db, User, Post, Tag
# Users
user1 = User(first_name="Stevie", last_name="Burgett")
user2 = User(first_name="Jake", last_name="Compton")

db.session.add(user1)
db.session.add(user2)
db.session.commit()

user1 = User.query.filter_by(first_name ="Stevie").one()

# Create a post with one tag and post with two tags
tag1 = Tag(tag_name="Sad")
tag2 = Tag(tag_name="Rad")

post1 = Post(title='A super cool title', content="Wow this content is also super cool", user_id=user1.id)
post2 = Post(title="Sad and Rad dude", content="This content is sad and rad at the same time", user_id=user1.id)


db.session.add_all([tag1, tag2, post1, post2])
db.session.commit()
