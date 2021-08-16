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

    def test_user_signup(self):
        """Test if user create is working"""
        user = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        user = user.signup(username=user.username,email=user.email,password=user.password,image_url=user.image_url)

        db.session.commit()

        #test user id matches one in database after adding
        self.assertEqual(user.id,User.query.get(user.id).id)
        
        #match password with user password after adding entry
        self.assertEqual(user.password,User.query.get(user.id).password)
        

    def test_user_authenticate(self):
        """Test if user authenticate is working"""
        user = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        User.signup(username=user.username,email=user.email,password=user.password,image_url=user.image_url)

        db.session.commit()

        #authenticate on success
        self.assertTrue(User.authenticate(username=user.username,password=user.password))

        #error on failure
        self.assertFalse(User.authenticate(username=user.username,password="badpassword"))

    def test_user_is_following(self):
        """Test if is following is working"""
        user1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        user2 = User(
            email = "test2@test.com",
            username = "testuser2",
            password = "another_password"
        )
        user1 = user1.signup(username=user1.username,password=user1.password,email=user1.email,image_url = user1.image_url)

        user2 = user2.signup(username=user2.username,password=user2.password,email=user2.email,image_url = user2.image_url)


        db.session.commit()

        follow_forward = Follows(user_being_followed_id=user1.id,user_following_id=user2.id)
        
        follow_backwords = Follows(user_being_followed_id=user2.id,user_following_id=user1.id)

        db.session.add(follow_backwords)
        db.session.add(follow_forward)

        db.session.commit()
        
        #check if user1 is following another
        self.assertTrue(user1.is_following(user2))

    def test_user_is_followed_by(self):
        """Test if is followed by is working"""

        user1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        user2 = User(
            email = "test2@test.com",
            username = "testuser2",
            password = "another_password"
        )
        user1 = user1.signup(username=user1.username,password=user1.password,email=user1.email,image_url = user1.image_url)

        user2 = user2.signup(username=user2.username,password=user2.password,email=user2.email,image_url = user2.image_url)


        db.session.commit()

        follow_forward = Follows(user_being_followed_id=user1.id,user_following_id=user2.id)
        
        follow_backwords = Follows(user_being_followed_id=user2.id,user_following_id=user1.id)

        db.session.add(follow_backwords)
        db.session.add(follow_forward)

        db.session.commit()
        
        #check if user1 is being followed by another
        self.assertTrue(user1.is_following(user2))
        
    def test_user_repr(self):
        """Test if repr function is working"""
        user1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        #test if reppr function shows accurate information
        self.assertEqual(f"{user1}",f"<User #{user1.id}: {user1.username}, {user1.email}>")
        