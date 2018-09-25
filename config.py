import ast
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Base:
    """
    Base configuration settings.
    """

    DEBUG = ast.literal_eval(os.getenv('DEBUG'))
    TESTING = ast.literal_eval(os.getenv('TESTING'))
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
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


class ProductionConfig(Base):
    """
    Production configuration settings.
    """

    pass


class DevelopmentConfig(Base):
    """
    Development configuration settings.
    """

    pass


class TestingConfig(Base):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tests.db')


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
