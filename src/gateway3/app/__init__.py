from .helper.exception_handler import handle_exception_function
from .helper.helper_functions import https_redirect, set_hsts_header
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    @app.before_request
    def before_request_function():
        # Initialize or recreate the database tables

        return https_redirect()

    # Import and register Blueprints
    # Assuming you have an auth blueprint for authentication

    # Ensure the SQLAlchemy session is closed when app context ends

    @app.after_request
    def after_request_function(response):
        response = set_hsts_header(response)
        return response

    @app.errorhandler(Exception)
    def handle_exception(error):
        response = handle_exception_function(error)
        return response

    with app.app_context():
        from .apis.apis import gateway_blueprint
        app.register_blueprint(gateway_blueprint, url_prefix='/dreamfair')

        return app
