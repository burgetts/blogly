from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class Blogly(TestCase):
    """Tests for Blogly app""" 

    def setUp(self):
        """Clean up any existing users and create test user."""
        User.query.delete()
        Post.query.delete()

        user = User(first_name="Stevie", last_name="Burgett")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up transactions"""
        db.session.rollback()
  
    def test_users_list(self):
        """Test that list of users is displayed on /users"""
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertIn('Users', html)
            self.assertIn("Stevie Burgett", html)

    def test_add_user(self):
        """Test that new user is added to list"""
        with app.test_client() as client:
            data = {"first_name": "Jake", "last_name": "C", "image": "None"}
            resp = client.post('/users/new', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("Users", html)
            self.assertIn("Stevie Burgett", html)
            self.assertIn("Jake C", html)


    def test_delete_user(self):
        """Test that delete user removes user from list"""
        with app.test_client() as client:
            data = {"first_name": "Stevie", "last_name": "Burgett", "image": "https://everydaynutrition.co.uk/wp-content/uploads/2015/01/default-user-avatar.png"}
            resp = client.post(f'/users/{self.user_id}/delete', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("Users", html)
            self.assertNotIn("Stevie Burgett", html)

    def test_user_details(self):
        """Test that user detail page comes up."""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertIn("<h2> Stevie Burgett", html)
        
        with app.test_client() as client:
            resp = client.get(f'/users/999999')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 404)

    def test_post_deletion(self):
        """Test that post is deleleted"""
        user = User.query.get(self.user_id)
        post = Post(title='A Super Awesome Post', content='This post is super duper awesome', user_id=user.id)
        db.session.add(post)
        db.session.commit()

        with app.test_client() as client:
            
            resp = client.post(f'/posts/{post.id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('id="profile_picture"', html)
            self.assertNotIn("A Super Awesome Post", html)

    def test_post_displayed_on_user_details(self):
        user = User.query.get(self.user_id)
        post = Post(title='A Super Awesome Post', content='This post is super duper awesome', user_id=user.id)
        db.session.add(post)

        with app.test_client() as client:
            resp = client.get(f'/users/{user.id}')
            html = resp.get_data(as_text=True)

            self.assertIn("A Super Awesome Post", html)

    # Post add form shows up correctly 
    def test_add_story_form(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)

            self.assertIn("Add Post For", html)

    
