from flask_restful import Resource

from .services import (
    OrganisationService,
    UserService,
    UserSessionService
)
from .validation import (
    create_verification_parser,
    edituserdetails_parser,
    login_parser,
    logout_parser,
    new_organisation_parser,
    registration_parser,
    update_verification_parser
)


class OrganisationResource(Resource):
    """
    Organisation resource.
    """

    def post(self):
        """
        Create a new organisation.
        """
        org_service = OrganisationService()
        user_service = UserService()

        data = new_organisation_parser.parse_args()
        org = org_service.exists(data['organisationName'])
        user = user_service.filter_by_uuid(data['keyCloakId'])

        if org:
            return {'message': 'Organisation already exists'}, 400

        if user is None:
            return {'message': 'User not registered'}, 400

        org = org_service.create_organisation(data['organisationName'], user)
        return {'organisationName': org.name, 'owner': org.owner.email}, 201


class UserResource(Resource):
    """
    Resource to create a user.
    """

    def post(self):
        service = UserService()
        data = registration_parser.parse_args()
        user = service.filter_by_uuid(data['tokenId'])

        # check if the user already exists
        if user is not None:
            return {'message': 'User already registered'}, 400

        new_user = service.create_user(data)
        return {'tokenId': new_user.uuid}, 201

class UserDetailResource(Resource):
    """
    User detail resource (retrieve, update, delete user).
    """

    def get(self, uuid):
        service = UserService()
        user = service.filter_by_uuid(uuid)

        # what if the user does not exist?
        if user is None:
            return {'message': 'User not found'}, 404
        # user found
        return {'firstName': user.first_name, 'lastName': user.last_name, 'email': user.email}, 200
        # pass

    def patch(self, uuid):
        service = UserService()
        data = edituserdetails_parser.parse_args()
        user = service.filter_by_uuid(uuid)

        if user is None:
            return {'message': 'User not found'}, 404

        service.update_user(user, data)
        return {}, 200


class UserLoginResource(Resource):
    """
    Resource to login a user.

    The API should return user details
    (last login time, failed log in attempts since last login)
    """

    def post(self, uuid):
        user_service = UserService()
        service = UserSessionService()
        data = login_parser.parse_args()

        user = user_service.filter_by_uuid(uuid)

        if user is None:
            return {'message': 'User not registered'}, 400

        service.record_login(user, data)

        # TODO: needs to return the number of failed login attempts
        # since the last successful login
        return {}, 201


class UserLogoutResource(Resource):
    """
    User Logout Resource.
    """

    def put(self, uuid):
        """
        Find the latest user session where the logout
        date is empty and update the logout date
        """
        user_service = UserService()
        service = UserSessionService()
        data = logout_parser.parse_args()

        user = user_service.filter_by_uuid(uuid)

        if user is None:
            return {'message': 'User not registered'}, 400

        service.update_login(user, data)
        return {}, 201


class UserCreateVerificationResource(Resource):
    def post(self, uuid):
        service = UserService()
        user = service.filter_by_uuid(uuid)

        if user is None:
            return {'message': 'User not registered'}, 400

        data = create_verification_parser.parse_args()
        service.create_verification(user, data)
        return {}, 201


class UserUpdateVerificationResource(Resource):
    def put(self, uuid):
        service = UserService()
        user = service.filter_by_uuid(uuid)

        if user is None:
            return {'message': 'User not registered'}, 400

        data = update_verification_parser.parse_args()
        user = service.update_verification(user, data)
        return {'tokenId': user.uuid, 'state': user.state}, 201
