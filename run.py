import os

from src import create_app
from src.api_0_1_0.models import Organisation, User, UserSession
from src.extensions import db

config_name = os.getenv('FLASK_ENV')
app = create_app(config_name)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Organisation': Organisation,
        'User': User,
        'UserSession': UserSession,
    }


if __name__ == '__main__':
    app.run('0.0.0.0')
