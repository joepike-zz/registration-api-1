from src.extensions import db
from .models import User, UserSession


class UserService:

    @staticmethod
    def create_user(data):
        """
        Create a user.

        :param data: a dict
        :return:     a User object
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
        """
        Update user once the verification email is sent.

        :param user: a User object
        :param data: a dict
        """
        user.state = data['state']
        user.email_sent_date = data['issuedTimestamp']
        user.email_sent = True
        db.session.commit()

    @staticmethod
    def filter_by_email(email):
        """
        Return a user object filtered by email.

        :param email: an email address
        :return:      a User object
        """
        return User.query.filter_by(email=email).first()

    @staticmethod
    def filter_by_uuid(uuid):
        """
        Return a user object filtered by uuid.

        :param uuid: a str representing a uuid
        :return:     a User object
        """
        return User.query.filter_by(uuid=uuid).first()

    @staticmethod
    def update_verification(user, data):
        """
        Update user state once the user verifies the verification email.

        :param user: a User object
        :param data: a dict
        :return:     a User object
        """
        user.state = data['state']
        db.session.commit()
        return user


class UserSessionService:

    @staticmethod
    def record_login(user, data):
        """
        Create a new login record.

        :param user: a User object
        :param data: a `dict` object
        """
        # TODO: needs to return the number of failed login attempts
        # since the last successful login
        user_session = UserSession(
            uuid=data['tokenId'],
            login_state=data['loginState'],
            login_date=data['loginDate'],
            user_id=user.id
        )
        db.session.add(user_session)
        db.session.commit()

    @staticmethod
    def update_login(user, data):
        """
        Once the user logs out, update the logout date.

        :param user: a User object
        :param data: a dict
        """
        session = UserSession.query.filter(UserSession.uuid == user.uuid)\
                                   .filter(UserSession.logout_date == None)\
                                   .first()
        session.logout_date = data['logoutDate']
        db.session.commit()
