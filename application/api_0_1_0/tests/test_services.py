import mock
import unittest

from flask_testing import TestCase

from application import create_app
from application.extensions import db
from application.api_0_1_0.models import User
from application.api_0_1_0.services import UserService


class TestServices(TestCase):
    def create_app(self):
        return create_app('testing')

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        data = {
            'email': 'json.adams@mail.com',
            'username': 'json',
            'first_name': 'Jason',
            'last_name': 'Adams'
        }

        service = UserService()
        new_user = service.create_user(data)

        self.assertEqual(new_user.email, data['email'])
        self.assertEqual(new_user.id, 1)
        self.assertTrue(isinstance(new_user, User))
        

if __name__ == '__main__':
    unittest.main()
