import os

from flask import Flask

from flaskr.exceptions import ConfigError


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', default=None),
        SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get(
            'SQLALCHEMY_TRACK_MODIFICATIONS', default=False),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI', default=None)
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    if app.config['SECRET_KEY'] is None:
        raise ConfigError("SECRET_KEY is not defined")
    if app.config['SQLALCHEMY_DATABASE_URI'] is None:
        raise ConfigError("SQLALCHEMY_DATABASE_URI is not defined")

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
