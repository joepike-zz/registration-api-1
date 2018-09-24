import os

from application import create_app
from application.extensions import db
from application.api_0_1_0.models import User


config_name = os.getenv('ENVIRONMENT')
app = create_app(config_name)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


if __name__ == '__main__':
    app.run('0.0.0.0')
