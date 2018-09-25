from flask_restful import Resource

from .serializers import user_detail_schema
from .services import UserService, UserSessionService
from .validation import (
    create_verification_parser,
    login_parser,
    registration_parser,
    update_verification_parser
)


class UserCreationResource(Resource):
    """
    Resource to create a user.
    """

    def post(self):
        service = UserService()
        data = registration_parser.parse_args()
        user = service.filter_by_uuid(data['tokenId'])

        # check if the user already exists
        if user is not None:
            return {'message': 'User already registered'}

        new_user = service.create_user(data)
        return {'tokenId': new_user.uuid}, 201


class UserLoginResource(Resource):
    """
    Resource to login a user.

    The API should return user details
    (last login time, failed log in attempts since last login)
    """

    def post(self, uuid):
        service = UserSessionService()
        data = login_parser.parse_args()

        # user.state = verified
        return {'lastLoginDateTime': user.last_login_datetime}


class UserLogoutResource(Resource):
    """
    Resource to logout a user.

    API updates the last login time.
    """

    def post(self, uuid):
        pass


class UserCreateVerificationResource(Resource):
    def post(self, uuid):
        user_service = UserService()
        session_service = UserSessionService()
        user = user_service.filter_by_uuid(uuid)

        if user is None:
            return {'message': 'User not registered'}

        data = create_verification_parser.parse_args()
        session_service.create_verification(user, data)
        return {}, 201


class UserUpdateVerificationResource(Resource):
    def put(self, uuid):
        service = UserSessionService()
        user_session = service.filter_by_uuid(uuid)

        if user_session is None:
            return {'message': 'User session does not exist'}

        data = update_verification_parser.parse_args()
        session = service.update_verification(user_session, data)
        return {'tokenId': session.uuid, 'state': session.state}


class UserResource(Resource):
    """
    Resource to retrieve, update and delete users.
    """

    def get(self, id):
        service = UserService()
        user = service.filter_by_id(id)

        # check if user exists
        if user is None:
            return {'message': 'User not found'}, 404

        result = user_detail_schema(user)
        return result

    def put(self):
        pass

    def delete(self):
        pass
