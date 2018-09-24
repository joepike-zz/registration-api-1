from application.extensions import db
from .models import User


class UserService:
    @staticmethod
    def filter_by_username(username):
        """
        Return a user object filtered by username.
        """
        return User.query.filter_by(username=username).first()

    @staticmethod
    def create_user(data):
        """
        Create a user object.
        """
        user = User(**data)
        # user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def filter_by_id(id):
        """
        Return a user object filtered by ID.
        """
        return User.query.filter_by(id=id).first()

    @staticmethod
    def verify_auth_token(username_or_token):
        return User.verify_auth_token(username_or_token)
