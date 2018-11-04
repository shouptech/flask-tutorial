import os
import tempfile
from datetime import datetime

import pytest
from werkzeug.security import generate_password_hash

from flaskr import create_app
from flaskr.db import init_db, db, User, Post

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SECRET_KEY': 'testing',
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///{}'.format(db_path)
    })

    with app.app_context():
        init_db()
        db.session.add(User(username='test',
                            password=generate_password_hash('test')))
        db.session.add(Post(title='test title',
                            body='test\nbody',
                            user_id=1,
                            created=datetime(year=2018,month=1,day=1)))
        db.session.commit()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
