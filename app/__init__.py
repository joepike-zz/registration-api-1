
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/user/', methods=['POST', 'GET'])
    def createUser():
        if request.method == "POST":
            email = str(request.data.get('Email'))
            content = request.json
            if email:
                userregistration = User(email=email,
                                        FisrtName=content['FirstName'],
                                        LastName=content['LastName'],
                                        KeyCloakId=content['keyCloakId'],
                                        State=content['State'],
                                        Created_at=content['Created_at'])
                userregistration.save()
                response = jsonify({
                    'id': userregistration.Id,
                })
                response.status_code = 201
                return response
            else:
                response.status = 400
                return {'message': 'Invalid input data provided'}

    @app.route('/user/<uuid>/createverification', method=['POST', 'GET'])
    def createverification():
        if request.method == "POST":
            VerificationTokenId = str(request.data.get('VerificationTokenId'))
            content = request.json
            if VerificationTokenId:
                userverify = verification(VerificationTokenId=VerificationTokenId,
                                          UserId=content['UserId'],
                                          IssuedTimestamp=content['IssuedTimestamp'],
                                          State=content['State'])
                userverify.save()
            else:
                response.status = 400
                return {'message': 'Invalid input data provided'}

    @app.route('/user/<uuid>/updateverfication', method=['PUT'])
    def updateverification():
        if request.method == "PUT":
            VerificationTokenId = str(request.data.get('VerificationTokenId'))
            content = request.json
            if VerificationTokenId:
                user = verification.query.filter_by('VerificationTokenId')
                userverify = verification(VerificationTokenId=VerificationTokenId,
                                          State=content['State'])

                response = jsonify({
                    'VerificationTokenId': verification.VerificationTokenId,
                    'State': verification.State
                })
                response.status_code = 201
                return response
            else:
                response.status = 400
                return {'message': 'Invalid input data provided'}

    @app.route('/user/<uuid>/recorduserlogin/', methods=['POST'])
    def recorduserlogin():
        if request.method == "POST":
            UserId = str(request.data.get('UserId'))
            content = request.json
            if UserId:
                userlogin = UserLogin(UserId=UserId,
                                      LoginState=content['LoginState'],
                                      LoginDate=content['LoginDate'],
                                      LogoutDate=Null)

                response = jsonify({
                    'UserId': userlogin.UserId,
                    'LoginState': userlogin.LoginState,
                    'LoginDate': userlogin.LoginDate
                })
                response.status_code = 201
                return response
            else:
                response.status = 400
                return {'message': 'Invalid input data provided'}

    @app.route('/user/<uuid>/updatseuserlogin/', methods=['PUT'])
    def updateuserlogin():
        if request.method == "PUT":
            UserId = str(request.data.get('UserId'))
            content = request.json
            if UserId:
                logoutuser = UserLogin.query.filter_by(UserId='UserId')
                userlogin = UserLogin(UserId=UserId,
                                      LoginState=content['LoginState'],
                                      LoginDate=content['LoginDate'])

                response = jsonify({
                    'UserId': userlogin.UserId,
                    'LoginState': userlogin.LoginState,
                    'LoginDate': userlogin.LoginDate
                })
                response.status_code = 201
                return response
            else:
                response.status = 400
                return {'message': 'Invalid input data provided'}




    return app
