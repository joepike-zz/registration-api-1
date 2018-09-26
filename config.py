import ast
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Base:
    """
    Base configuration settings.
    """

    DEBUG = ast.literal_eval(os.getenv('DEBUG'))
    TESTING = ast.literal_eval(os.getenv('TESTING'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Base):
    """
    Production configuration settings.
    """

    DBUSER = os.getenv('DBUSER')
    DBPASSWORD = os.getenv('DBPASSWORD')
    DBHOST = os.getenv('DBHOST')
    DBNAME = os.getenv('DBNAME')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
        DBUSER,
        DBPASSWORD,
        DBHOST,
        DBNAME
    )


class DevelopmentConfig(Base):
    """
    Development configuration settings.
    """

    SQLALCHEMY_DATABASE_URI = 'postgresql://user:test@database/egar'


class TestingConfig(Base):
    """
    Testing configuration settings.
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:test@test_database/test_egar'


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
