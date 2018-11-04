import pytest

from flaskr import create_app
from flaskr.exceptions import ConfigError


@pytest.mark.parametrize('config', (
    {},
    {'SECRET_KEY':'test'}
))
def test_bad_config(config):
    try:
        create_app(config).testing
        assert False
    except ConfigError:
        assert True

def test_good_config():
    assert create_app(None)
