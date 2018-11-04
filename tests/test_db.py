import sqlite3

import pytest

from flaskr.db import Post, User

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called

def test_repr():
    user = User(username='test')
    assert 'test' in repr(user)

    post = Post(title='test')
    assert 'test' in repr(post)
