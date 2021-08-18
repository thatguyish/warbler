from unittest import TestCase
from os import environ
from models import db, Message, User, Follows

environ['DATABASE_URL'] = "postgres:///warbler_test"

from app import app

class TestMessageModel(TestCase):
    """Test the message model"""

    def setup(self):
        self.user = User.query.get_all()[0]
        self.message = Message(text="This is some text",user_id=self.user.id)

    def Test_Create_message(self):
        """Tests creation of a message model"""
        self.assertTrue(self.message)

    def Test_Message_correct(self):
        """Test if message gets saved correctly"""
        self.message = "This is changed text"
        self.assertEqual(self.message.text,"This is changed text")
    
    def Test_Time(self):
        """Test if Time is present"""
        self.assertTrue(self.message.timestamp)
