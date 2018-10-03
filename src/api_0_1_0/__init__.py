from flask import Blueprint
from flask_restful import Api


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


from . import routes


api.add_resource(routes.UserCreationResource, '/users/registeruser')
api.add_resource(routes.UserLoginResource, '/users/<string:uuid>/recorduserlogin')
api.add_resource(routes.UserLogoutResource, '/users/<string:uuid>/updateuserlogin')
api.add_resource(routes.UserCreateVerificationResource, '/users/<string:uuid>/createverification')
api.add_resource(routes.UserUpdateVerificationResource, '/users/<string:uuid>/updateverification')

# organisations
api.add_resource(routes.OrganisationResource, '/organisations')
