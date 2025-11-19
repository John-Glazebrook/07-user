# python -m flask --app hyprnews run
# python -m flask --app hyprnews init-db

from flask import Flask
from .models import db#, migrate
import os
import click

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///hyprnews.v2.sqlite.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    # migrate.init_app(app, db)

    if test_config is None:
        # load the instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        # test config
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # db.init_app(app)
    @app.cli.command('init-db')
    @click.option('--empty', is_flag=True, help="Create schema only, no mock data")
    def init_db_command(empty):
        """Clear the existing data and create new tables."""
        with app.app_context():
            db.create_all()
            if not empty:
                from . import mockdata
                mockdata.seed_db(db)
        click.echo('Initialized the database' + ('' if empty else ' with mock data.'))

    #
    # BLUEPRINTS
    #
    from . import auth
    app.register_blueprint(auth.bp)
    #app.add_url_rule('/', endpoint='index')

    from . import news
    app.register_blueprint(news.bp)
    app.add_url_rule('/', endpoint='index')

    return app

