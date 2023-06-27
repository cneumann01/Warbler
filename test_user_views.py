from unittest import TestCase
from models import User, Message, Follows
from app import app, db, CURR_USER_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler-test'
app.config['SQLALCHEMY_ECHO'] = False

class UserViewsTestCase(TestCase):
    """Test views for user."""

    def setUp(self):
        """Create test client, add sample data."""

        self.app = app.app_context()
        self.app.push()
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.user1 = User.signup("user1", "user1@test.com", "password", None)
        self.user2 = User.signup("user2", "user2@test.com", "password", None)

        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_followers_page_logged_in(self):
        """Can you see the follower page when logged in?"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.get(f"/users/{self.user1.id}/followers")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Followers", str(resp.data))

    def test_followers_page_logged_out(self):
        """Are you disallowed from visiting a user's follower page when logged out?"""

        with self.client as client:
            resp = client.get(f"/users/{self.user1.id}/followers", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Followers", str(resp.data))
            self.assertIn("Access unauthorized.", str(resp.data))

    def test_following_page_logged_in(self):
        """Can you see the following page when logged in?"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.get(f"/users/{self.user1.id}/following")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Following", str(resp.data))

    def test_following_page_logged_out(self):
        """Are you disallowed from visiting a user's following page when logged out?"""

        with self.client as client:
            resp = client.get(f"/users/{self.user1.id}/following", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Following", str(resp.data))
            self.assertIn("Access unauthorized.", str(resp.data))

    def test_add_message_logged_in(self):
        """Can you add a message when logged in?"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.post("/messages/new", data={"text": "Test message"}, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test message", str(resp.data))

    def test_add_message_logged_out(self):
        """Are you prohibited from adding messages when logged out?"""

        with self.client as client:
            resp = client.post("/messages/new", data={"text": "Test message"}, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Test message", str(resp.data))
            self.assertIn("Access unauthorized.", str(resp.data))

    def test_delete_message_logged_in(self):
        """Can you delete a message when logged in?"""

        message = Message(text="Test message", user_id=self.user1.id)
        db.session.add(message)
        db.session.commit()

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.post(f"/messages/{message.id}/delete", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Test message", str(resp.data))

    def test_delete_message_logged_out(self):
        """Are you prohibited from deleting messages when logged out?"""

        message = Message(text="Test message", user_id=self.user1.id)
        db.session.add(message)
        db.session.commit()

        with self.client as client:
            resp = client.post(f"/messages/{message.id}/delete", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", str(resp.data))
            

    def test_delete_message_as_another_user(self):
        """Are you prohibited from deleting a message as another user?"""

        message = Message(text="Test message", user_id=self.user2.id)
        db.session.add(message)
        db.session.commit()

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.post(f"/messages/{message.id}/delete", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", str(resp.data))
            self.assertIn("Test message", str(resp.data))
