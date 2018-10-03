import mock
import unittest

from datetime import datetime
from flask_testing import TestCase

from src import create_app
from src.extensions import db
from src.api_0_1_0.models import Organisation, User
from src.api_0_1_0.services import UserService


class TestServices(TestCase):
    def create_app(self):
        return create_app('testing')

    def setUp(self):
        db.create_all()
        self.data1 = {
            'email': 'json.adams@mail.com',
            'firstName': 'Jason',
            'lastName': 'Adams',
            'tokenId': 'b3309c34-c055-11e8-a2eb-0242ac120003',
        }
        self.user1 = User(
            email=self.data1['email'],
            first_name=self.data1['firstName'],
            last_name=self.data1['lastName'],
            uuid=self.data1['tokenId']
        )
        self.organisation1 = Organisation(
            name='Aker Systems',
            owner=self.user1
        )
        db.session.add_all([self.user1, self.organisation1])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_organisation_creation(self):
        data = {
            "keyCloakId": "b3309c34-c055-11e8-a2eb-0242ac120003",
            "organisationName": "Tesla Motors"
        }
        res = self.client.post('/v0.1.0/organisations', data=data)

        self.assertEqual(res.status, '201 CREATED')
        self.assertEqual(res.json['organisationName'], data['organisationName'])
        self.assertEqual(res.json['owner'], self.user1.email)

    def test_organisation_already_exists(self):
        data = {
            "keyCloakId": "b3309c34-c055-11e8-a2eb-0242ac120003",
            "organisationName": "Aker Systems"
        }
        res = self.client.post('/v0.1.0/organisations', data=data)

        self.assertEqual(res.status, '400 BAD REQUEST')
        self.assertEqual(res.json['message'], 'Organisation already exists')

    def test_organisation_user_not_registered(self):
        data = {
            "keyCloakId": "12345-c055-11e8-a2eb-0242ac120003",
            "organisationName": "Tesla Motors"
        }
        res = self.client.post('/v0.1.0/organisations', data=data)

        self.assertEqual(res.status, '400 BAD REQUEST')
        self.assertEqual(res.json['message'], 'User not registered')

    def test_user_creation_resource(self):
        data = {
            "email": "mike@mail.com",
            "firstName": "Mike",
            "lastName": "Adams",
            "tokenId": "b16d4104-c055-11e8-a2eb-0242ac120003"
        }
        res = self.client.post('/v0.1.0/users/registeruser', data=data)

        self.assertEqual(res.status, '201 CREATED')
        self.assertEqual(res.json['tokenId'], data['tokenId'])
        self.assertTrue('tokenId' in res.json)

    def test_user_creation_resource_with_existing_user(self):
        res = self.client.post('/v0.1.0/users/registeruser', data=self.data1)

        self.assertEqual(res.status, '400 BAD REQUEST')
        self.assertEqual(res.json['message'], 'User already registered')

    def test_user_create_verification_resource(self):
        params = {
            "tokenId": "b3309c34-c055-11e8-a2eb-0242ac120003",
            "userId": 1,
            "issuedTimestamp": "2018-09-24 23:33:20",
            "state": "Unverified"
        }
        res = self.client.post('/v0.1.0/users/b3309c34-c055-11e8-a2eb-0242ac120003/createverification', data=params)

        self.assertEqual(res.status, '201 CREATED')

    def test_user_create_verification_resource_with_unregistered_user(self):
        params = {
            "tokenId": "b16d4104-c055-11e8-a2eb-0242ac120003",
            "userId": 1,
            "issuedTimestamp": "2018-09-24 23:33:20",
            "state": "Unverified"
        }
        res = self.client.post('/v0.1.0/users/b16d4104-c055-11e8-a2eb-0242ac120003/createverification', data=params)

        self.assertEqual(res.status, '400 BAD REQUEST')
        self.assertEqual(res.json['message'], 'User not registered')

    def test_user_update_verification_resource(self):
        params = {
            "tokenId": "b3309c34-c055-11e8-a2eb-0242ac120003",
            "state": "Verified"
        }
        res = self.client.put('/v0.1.0/users/b3309c34-c055-11e8-a2eb-0242ac120003/updateverification', data=params)

        self.assertEqual(res.status, '201 CREATED')
        self.assertEqual(res.json['state'], 'Verified')

    def test_user_update_verification_resource_with_unregistered_user(self):
        params = {
            "tokenId": "b16d4104-c055-11e8-a2eb-0242ac120003",
            "state": "Verified"
        }
        res = self.client.put('/v0.1.0/users/b16d4104-c055-11e8-a2eb-0242ac120003/updateverification', data=params)

        self.assertEqual(res.status, '400 BAD REQUEST')
        self.assertEqual(res.json['message'], 'User not registered')

    def test_user_login_resource(self):
        params = {
            "tokenId": "b3309c34-c055-11e8-a2eb-0242ac120003",
            "loginState": "success",
            "loginDate": "2018-09-24 20:33:20"
        }
        res = self.client.post('/v0.1.0/users/b3309c34-c055-11e8-a2eb-0242ac120003/recorduserlogin', data=params)

        self.assertEqual(res.status, '201 CREATED')

    def test_user_login_resource_with_unregistered_user(self):
        params = {
            "tokenId": "b16d4104-c055-11e8-a2eb-0242ac120003",
            "loginState": "success",
            "loginDate": "2018-09-24 20:33:20"
        }
        res = self.client.post('/v0.1.0/users/b16d4104-c055-11e8-a2eb-0242ac120003/recorduserlogin', data=params)

        self.assertEqual(res.status, '400 BAD REQUEST')
        self.assertEqual(res.json['message'], 'User not registered')

    def test_user_logout_resource(self):
        # first we need to create the login
        params = {
            "tokenId": "b3309c34-c055-11e8-a2eb-0242ac120003",
            "loginState": "success",
            "loginDate": "2018-09-24 20:33:20"
        }
        res = self.client.post('/v0.1.0/users/b3309c34-c055-11e8-a2eb-0242ac120003/recorduserlogin', data=params)

        self.assertEqual(res.status, '201 CREATED')

        params = {
            "logoutDate": "2018-09-25 10:33:20"
        }
        res = self.client.put('/v0.1.0/users/b3309c34-c055-11e8-a2eb-0242ac120003/updateuserlogin', data=params)

        self.assertEqual(res.status, '201 CREATED')

    def test_user_logout_resource_with_unregistered_user(self):
        params = {
            "logoutDate": "2018-09-25 10:33:20"
        }
        res = self.client.put('/v0.1.0/users/b16d4104-c055-11e8-a2eb-0242ac120003/updateuserlogin', data=params)

        self.assertEqual(res.status, '400 BAD REQUEST')
        self.assertEqual(res.json['message'], 'User not registered')


if __name__ == '__main__':
    unittest.main()
