import mock
import unittest

from datetime import datetime
from flask_testing import TestCase

from src import create_app
from src.extensions import db
from src.api_0_1_0.models import (
    Organisation,
    User,
    UserSession
)
from src.api_0_1_0.services import (
    OrganisationService,
    UserService,
    UserSessionService
)


class TestOrganisationService(TestCase):
    def create_app(self):
        return create_app('testing')

    def setUp(self):
        db.create_all()
        self.organisation1 = Organisation(name='Aker Systems')
        self.user1 = User(
            email='json.adams@mail.com',
            first_name='Jason',
            last_name='Adams',
            uuid='b3309c34-c055-11e8-a2eb-0242ac120003'
        )
        db.session.add_all([self.organisation1, self.user1])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_organisation(self):
        service = OrganisationService()
        organisation = service.create_organisation('NASA', self.user1)

        self.assertTrue(isinstance(organisation, Organisation))
        self.assertEqual(organisation.name, 'NASA')
        self.assertEqual(organisation.owner, self.user1)

    def test_organisation_exists(self):
        service = OrganisationService()
        organisation = service.exists('Aker Systems')

        self.assertTrue(organisation)

    def test_organisation_does_not_exist(self):
        service = OrganisationService()
        organisation = service.exists('Tesla Motors')

        self.assertFalse(organisation)


class TestUserService(TestCase):
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
        self.data2 = {
            'email': 'mike.roberts@mail.com',
            'firstName': 'Mike',
            'lastName': 'Roberts',
            'tokenId': 'b6603c58-c055-11e8-a2eb-0242ac070001',
        }
        user1 = User(
            email=self.data1['email'],
            first_name=self.data1['firstName'],
            last_name=self.data1['lastName'],
            uuid=self.data1['tokenId']
        )
        user2 = User(
            email=self.data2['email'],
            first_name=self.data2['firstName'],
            last_name=self.data2['lastName'],
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
            'tokenId': 'b16d4104-c055-11e8-a2eb-0242ac120003',
        }
        service = UserService()
        new_user = service.create_user(data)

        self.assertEqual(new_user.uuid, data['tokenId'])
        self.assertEqual(new_user.email, data['email'])
        self.assertTrue(new_user.state is None)
        self.assertTrue(isinstance(new_user, User))

    def test_update_user(self):
        data = {
            'email': 'kevin.smith@mail.com',
            'firstName': 'Kevin',
            'lastName': 'Smith'
        }
        service = UserService()
        user = service.filter_by_uuid(self.data1['tokenId'])

        self.assertEqual(user.first_name, self.data1['firstName'])
        self.assertEqual(user.last_name, self.data1['lastName'])

        updated_user = service.update_user(user, data)

        self.assertEqual(updated_user.email, data['email'])
        self.assertEqual(updated_user.first_name, data['firstName'])
        self.assertEqual(updated_user.last_name, data['lastName'])

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


class TestUserSessionService(TestCase):
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
        user1 = User(
            email=self.data1['email'],
            first_name=self.data1['firstName'],
            last_name=self.data1['lastName'],
            uuid=self.data1['tokenId']
        )
        db.session.add(user1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_record_login(self):
        data = {
            "tokenId": "b3309c34-c055-11e8-a2eb-0242ac120003",
            "loginState": "success",
            "loginDate": "2018-09-24 20:33:20"
        }
        service = UserSessionService()
        user_service = UserService()

        # checks that user session has no recorded logins
        user_sessions = UserSession.query.all()
        self.assertEqual(user_sessions, [])

        user = user_service.filter_by_uuid(self.data1['tokenId'])
        service.record_login(user, data)

        user_session = UserSession.query.first()
        login_date_object = datetime.strptime(data['loginDate'], '%Y-%m-%d %H:%M:%S')

        self.assertEqual(user_session.uuid, user.uuid)
        self.assertEqual(user_session.login_state, data['loginState'])
        self.assertEqual(user_session.login_date, login_date_object)

    def test_update_login(self):
        data = {
            "tokenId": "b3309c34-c055-11e8-a2eb-0242ac120003",
            "loginState": "success",
            "loginDate": "2018-09-24 20:33:20"
        }
        service = UserSessionService()
        user_service = UserService()

        # create a login
        user = user_service.filter_by_uuid(self.data1['tokenId'])
        service.record_login(user, data)

        # make sure logout date is None
        user_session = UserSession.query.first()
        self.assertTrue(user_session.logout_date is None)

        # update login with logout date
        service.update_login(user, {"logoutDate": "2018-09-25 10:33:20"})
        user_session = UserSession.query.first()
        logout_date_obj = datetime.strptime("2018-09-25 10:33:20", '%Y-%m-%d %H:%M:%S')

        self.assertEqual(user_session.logout_date, logout_date_obj)

if __name__ == '__main__':
    unittest.main()
