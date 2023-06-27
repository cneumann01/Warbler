import unittest
import os
from models import db, User, Message

# Set up the Flask app for testing
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

app.config['WTF_CSRF_ENABLED'] = False

# Define a class for testing the Message model
class MessageModelTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the test database before each test."""
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

            # Create a test user
            user = User(
                username='testuser',
                password='testpassword',
                email='test@example.com'
            )
            db.session.add(user)
            db.session.commit()

            # Set the user_id for the test messages
            self.user_id = user.id

    def tearDown(self):
        """Clean up the test database after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_message(self):
        """Test creating a new message."""
        with app.app_context():
            message = Message(text='This is a test message.', user_id=self.user_id)
            db.session.add(message)
            db.session.commit()

            retrieved_message = Message.query.filter_by(text='This is a test message.').first()

            self.assertIsNotNone(retrieved_message)
            self.assertEqual(retrieved_message.text, 'This is a test message.')

    def test_delete_message(self):
        """Test deleting a message."""
        with app.app_context():
            message = Message(text='This is a test message.', user_id=self.user_id)
            db.session.add(message)
            db.session.commit()

            db.session.delete(message)
            db.session.commit()

            deleted_message = Message.query.filter_by(text='This is a test message.').first()

            self.assertIsNone(deleted_message)

if __name__ == '__main__':
    unittest.main()
