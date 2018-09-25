import mock
import unittest

from datetime import datetime
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
        self.data1 = {
            'email': 'json.adams@mail.com',
            'firstName': 'Jason',
            'lastName': 'Adams',
            'password': 'super123',
            'tokenId': 'b3309c34-c055-11e8-a2eb-0242ac120003',
        }
        self.data2 = {
            'email': 'mike.roberts@mail.com',
            'firstName': 'Mike',
            'lastName': 'Roberts',
            'password': 'test333',
            'tokenId': 'b6603c58-c055-11e8-a2eb-0242ac070001',
        }
        user1 = User(
            email=self.data1['email'],
            first_name=self.data1['firstName'],
            last_name=self.data1['lastName'],
            password=self.data1['password'],
            uuid=self.data1['tokenId']
        )
        user2 = User(
            email=self.data2['email'],
            first_name=self.data2['firstName'],
            last_name=self.data2['lastName'],
            password=self.data2['password'],
            uuid=self.data2['tokenId']
        )
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_filter_by_email(self):
        service = UserService()
        user = service.filter_by_email(self.data1['email'])

        self.assertEqual(user.uuid, self.data1['tokenId'])
        self.assertEqual(user.email, self.data1['email'])
        self.assertTrue(isinstance(user, User))

    def test_filter_by_uuid(self):
        service = UserService()
        user = service.filter_by_uuid(self.data1['tokenId'])

        self.assertEqual(user.email, self.data1['email'])
        self.assertEqual(user.uuid, self.data1['tokenId'])

    def test_create_user(self):
        data = {
            'email': 'susan.felix@mail.com',
            'firstName': 'Susan',
            'lastName': 'Felix',
            'password': 'admin123',
            'tokenId': 'b16d4104-c055-11e8-a2eb-0242ac120003',
        }
        service = UserService()
        new_user = service.create_user(data)

        self.assertEqual(new_user.uuid, data['tokenId'])
        self.assertEqual(new_user.email, data['email'])
        self.assertTrue(new_user.state is None)
        self.assertTrue(isinstance(new_user, User))

    def test_create_verification(self):
        data = {
            'tokenId': 'b3309c34-c055-11e8-a2eb-0242ac120003',
            'userId': 1,
            'issuedTimestamp': '2018-09-21 20:33:20',
            'state': 'Unverified',
        }
        service = UserService()
        user = service.filter_by_uuid(self.data1['tokenId'])

        self.assertTrue(user.email_sent_date is None)
        self.assertTrue(user.state is None)

        service.create_verification(user, data)
        email_sent_date = datetime.strptime(data['issuedTimestamp'], '%Y-%m-%d %H:%M:%S')

        self.assertEqual(user.email_sent_date, email_sent_date)
        self.assertEqual(user.state, data['state'])

    def test_update_verification(self):
        data = {
            'tokenId': 'b3309c34-c055-11e8-a2eb-0242ac120003',
            'state': 'Verified'
        }
        service = UserService()
        user = service.filter_by_uuid(self.data1['tokenId'])
        user.email_sent_date = '2018-09-21 20:33:20'
        user.state = 'Unverified'
        db.session.commit()
        
        self.assertEqual(user.state, 'Unverified')

        service.update_verification(user, data)

        self.assertEqual(user.state, 'Verified')
if __name__ == '__main__':
    unittest.main()
