
# from sqlalchemy.dialects.postgresql import UUID

from application import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String(130))
    uuid = db.Column(db.String(130), unique=True)
    state = db.Column(db.String(30))
    email_sent = db.Column(db.Boolean, default=False)
    email_sent_date = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_updated = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    user_session = db.relationship(
        'UserSession',
        backref='user',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<User: {email} account: {state}>'.format(**self.__dict__)


class UserSession(db.Model):
    __tablename__ = 'usersession'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(130))
    login_date = db.Column(db.DateTime, nullable=True)
    logout_date = db.Column(db.DateTime, nullable=True)
    failed_login_attempts_since_last_login = db.Column(db.Integer)
    login_state = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<UserSession: {uuid}>'.format(**self.__dict__)
