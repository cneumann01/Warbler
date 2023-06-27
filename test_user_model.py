import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database)

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        self.app = app.app_context()
        self.app.push()
        db.create_all()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
        db.drop_all()

    def test_user_repr(self):
        """Does the repr method work as expected?"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()
        self.assertEqual(repr(u), "<User #1: testuser, test@test.com>")

    def test_user_is_following(self):
        """Does is_following successfully detect when user1 is following user2?"""
        user1 = User.signup("user1", "user1@test.com", "password", None)
        user2 = User.signup("user2", "user2@test.com", "password", None)
        db.session.commit()
        
        user1.following.append(user2)
        db.session.commit()

        self.assertTrue(user1.is_following(user2))
        self.assertFalse(user2.is_following(user1))

    def test_user_is_following_not_following(self):
        """Does is_following successfully detect when user1 is not following user2?"""
        user1 = User.signup("user1", "user1@test.com", "password", None)
        user2 = User.signup("user2", "user2@test.com", "password", None)
        db.session.commit()
        
        self.assertFalse(user1.is_following(user2))
        self.assertFalse(user2.is_following(user1))

    def test_user_is_followed_by(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?"""
        user1 = User.signup("user1", "user1@test.com", "password", None)
        user2 = User.signup("user2", "user2@test.com", "password", None)
        db.session.commit()
        
        user1.followers.append(user2)
        db.session.commit()

        self.assertTrue(user1.is_followed_by(user2))
        self.assertFalse(user2.is_followed_by(user1))

    def test_user_is_followed_by_not_followed(self):
        """Does is_followed_by successfully detect when user1 is not followed by user2?"""
        user1 = User.signup("user1", "user1@test.com", "password", None)
        user2 = User.signup("user2", "user2@test.com", "password", None)
        db.session.commit()
        
        self.assertFalse(user1.is_followed_by(user2))
        self.assertFalse(user2.is_followed_by(user1))

    def test_user_signup(self):
        """Does User.signup successfully create a new user given valid credentials?"""
        user = User.signup("testuser", "test@test.com", "password", None)
        db.session.commit()

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(User.authenticate("testuser", "password"))
