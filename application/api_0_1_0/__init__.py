from flask import Blueprint
from flask_restful import Api


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


from . import routes


api.add_resource(routes.UserCreationResource, '/user')
api.add_resource(routes.UserLoginResource, '/user/login')
api.add_resource(routes.UserLogoutResource, '/user/logout')
api.add_resource(routes.UserResource, '/user/<string:username>')
