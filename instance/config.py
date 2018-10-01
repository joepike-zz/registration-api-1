
import os

class Config(object):
    """Configuration class."""

    DEBUG = True
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class TestingConfig(Config):
    """Configurations for Testing, seperate test database."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://joe:password@localhost/test_db'
    DEBUG = True

app_config = {
    'testing': TestingConfig,
}
