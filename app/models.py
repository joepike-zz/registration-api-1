
from app import db

class User(db.Model):
    """This class represents the user registration table."""

    __tablename__ = 'user_registration'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, name):
        """Iniitialize with name."""
        self.username = name

    def save(self):
        db.session.add(self)
        db.session.commi()

    def __repr__(self):
        return "<UserRegistration: {}>".format(self.username)

class verification(db.Model):
    """This class represents the user verification table."""

    __tablename__ = 'user_registration'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, name):
        """Iniitialize with name."""
        self.username = name

    def save(self):
        db.session.add(self)
        db.session.commi()

    def __repr__(self):
        return "<UserRegistration: {}>".format(self.username)

class UserLogin(db.Model):
