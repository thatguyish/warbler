"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgres:///warbler_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""
    
    def setUp(self):
        """Create test client, add sample data."""

        Message.query.delete()
        User.query.delete()
        Follows.query.delete()

        self.client = app.test_client()


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        db.session.rollback()

    def test_user_signup(self):
        """Test if user create is working"""
        user = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        user = user.signup(username=user.username,email=user.email,password=user.password,image_url=user.image_url)

        db.session.commit()

        self.assertEqual(user.id,User.query.get(user.id).id)
        
        self.assertEqual(user.password,User.query.get(user.id).password)
        

    def test_user_authenticate(self):
        """Test if user authenticate is working"""

    def test_user_is_following(self):
        """Test if is following is working"""

        

    def test_user_is_followed_by(self):
        """Test if is followed by is working"""

    def test_user_repr(self):
        """Test if repr function is working"""
        