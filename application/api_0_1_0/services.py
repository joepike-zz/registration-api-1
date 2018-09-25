from application.extensions import db
from .models import User, UserSession


class UserService:
    @staticmethod
    def filter_by_email(email):
        """
        Return a user object filtered by email.
        """
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(data):
        """
        Create a user object.
        """
        user = User(
            email=data['email'],
            first_name=data['firstName'],
            last_name=data['lastName'],
            password=data['password'],
            uuid=data['tokenId']
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def create_verification(user, data):
        user.state = data['state']
        user.email_sent_date = data['issuedTimestamp']
        user.email_sent = True
        db.session.commit()
        return user

    @staticmethod
    def filter_by_uuid(uuid):
        """
        Return a user object filtered by uuid.
        """
        return User.query.filter_by(uuid=uuid).first()

    @staticmethod
    def update_verification(user, data):
        user.state = data['state']
        db.session.commit()
        return user

    @staticmethod
    def verify_auth_token(username_or_token):
        return User.verify_auth_token(username_or_token)


class UserSessionService:
    @staticmethod
    def filter_by_uuid(uuid):
        return UserSession.query.filter_by(uuid=uuid).first()

    

    # @staticmethod
    # def record_login(data):
    #     if data['loginState'] == 'failed':

    #         user_session = UserSession(
    #             uuid=data['tokenId'],
    #             login_state=data['loginState'],
    #             login_date=data['loginDate']
    #         )
