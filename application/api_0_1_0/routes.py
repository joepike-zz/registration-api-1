from flask_restful import Resource, reqparse

from .serializers import user_detail_schema
from .services import UserService


# validation parsers
create_parser = reqparse.RequestParser()
user_parser = reqparse.RequestParser()

# create user validation parser
create_parser.add_argument(
    'username',
    help='This field is required',
    required=True
)
create_parser.add_argument(
    'password',
    help='This field is required',
    required=True
)
create_parser.add_argument(
    'email',
    help='This field is required',
    required=True
)
create_parser.add_argument(
    'firstName',
    help='This field is required',
    required=True
)
create_parser.add_argument(
    'lastName',
    help='This field is required',
    required=True
)
create_parser.add_argument(
    'state',
    help='This field is required',
    required=True
)
# create_parser.add_argument(
#     'keyCloakId',
#     help='This field is required',
#     required=True
# )

# user validation parser
user_parser.add_argument(
    'username',
    help='This field is required',
    required=True
)


class UserCreationResource(Resource):
    """
    Resource to create a user.
    """

    def post(self):
        service = UserService()
        data = create_parser.parse_args()
        user = service.filter_by_username(data['username'])

        # check if the user already exists
        if user is not None:
            return {'message': 'User already registered'}

        self.service.create_user(data)
        return {'message': 'User created'}


class UserLoginResource(Resource):
    """
    Resource to login a user.
    """

    # def get(self):
    #     data = login_parser.parse_args()
    #     user = self.service.filter_by_username(data['username'])

    #     # check if user exists
    #     if user is None:
    #         return {'message': 'User not registered'}

    #     # check if password is correct
    #     if data['password'] == user.password:
    #         return {'message': 'Login successful'}

    #     return {'message': 'Incorrect credentials'}
    pass


class UserLogoutResource(Resource):
    """
    Resource to logout a user.
    """

    def get(self):
        pass


class UserResource(Resource):
    """
    Resource to retrieve, update and delete users.
    """

    def get(self, username):
        service = UserService()
        user = service.filter_by_username(username)

        # check if user exists
        if user is None:
            return {'message': 'User not found'}, 404

        result = user_detail_schema(user)
        return result

    def put(self):
        pass

    def delete(self):
        pass
