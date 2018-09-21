import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Base:
    """
    Base configuration settings.
    """

    DEBUG = os.getenv('DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
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


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig
}
