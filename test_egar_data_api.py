
import unittest
import os
import json
from app import create_app, db

class UserRegistrationTestCase(unittest.TestCase):
    """This class represents the user registration test case."""

    def setUp(self):
        """Defing test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.user_registration = {'username': 'Joe'}

        with self.app.app_context():
            db.create_all()

    def test_userregistration(self):
        """Test API can create a registered user (POST request)"""
        res = self.client.post('/user/', data=self.user_registration)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Joe', str(res.data))

    def test_userregistration(self):
        """Test API can create a registered user (POST request)"""
        res = self.client.post('/user/', data=self.user_registration)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Joe', str(res.data))

    def test_login(self):
        """Test API can log a user in (GET request)"""
        res = self.client.get('/')

    def tearDown(self):
        """teardown initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
