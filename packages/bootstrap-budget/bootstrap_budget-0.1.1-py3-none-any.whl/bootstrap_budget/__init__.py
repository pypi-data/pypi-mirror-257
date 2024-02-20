import importlib.metadata
import sqlite3

from flask import Flask
from logging.config import dictConfig

# Import Bootstrap Budget modules
from . import account
from . import admin
from . import auth
from . import budget
from . import budget_item
from . import dashboard
from . import db
from . import transaction
from . import user


# Set Bootstrap Budget version
__version__: str = importlib.metadata.version('bootstrap_budget')


dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def main() -> Flask:
    """
    The main function for Bootstrap Budget.

    :return: A Flask app (Bootstrap Budget)
    """
    # Create and configure the app
    # The instance folder is set to 'relative' in order to find the config file easily
    app = Flask(__name__, instance_relative_config=True)

    # Check to see if the database was set up through the CLI utility.
    with app.app_context():
        db_connection: sqlite3.Connection = db.get_db()

        if db_connection is None:
            raise RuntimeError('The Bootstrap Budget database has not been created. '
                               'Use the "bootstrap --setup" CLI command to complete the installation.')

    # Find the configuration file one level up from the instance folder (defined as relative)
    # A configuration file should have been created from the 'boostrap --setup' CLI and contain
    # the SECRET_KEY and any other configurations.
    app.config.from_pyfile('bootstrap_config.py')

    # Register Bootstrap Budget blueprints
    app.register_blueprint(account.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(budget.bp)
    app.register_blueprint(budget_item.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(transaction.bp)
    app.register_blueprint(user.bp)

    # Define the index entry point: The Boostrap Budget Dashboard
    app.add_url_rule("/", endpoint="dashboard.index")

    return app
