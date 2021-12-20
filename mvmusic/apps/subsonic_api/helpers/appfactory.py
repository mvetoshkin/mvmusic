import time

from flask import Flask, g
from sqlalchemy import event
from sqlalchemy.engine.base import Engine
from werkzeug.exceptions import HTTPException

from mvmusic.common.database import db
from mvmusic.common.exceptions import AccessDeniedError, AppException, \
    AppValueError, BadRequestError, NoExtensionException, NotFoundError, \
    UnauthorizedError
from mvmusic.common.exceptions import ModelKeyError
from mvmusic.common.utils import import_object
from mvmusic.settings import settings
from ..responses import get_resp_format, \
    get_subsonic_error_code, make_response


class AppFactory:
    __instance = None
    app = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(AppFactory, cls).__new__(cls)
            cls.__instance.__create_app()

        return cls.__instance

    def __create_app(self):
        self.app = Flask('mvmusic')
        self.app.config.from_object(settings)

        self.__bind_extensions()
        self.__register_blueprints()

    def __bind_extensions(self):
        for ext_path in self.app.config.get('EXTENSIONS', []):
            try:
                obj = import_object(ext_path)
            except ImportError:
                raise NoExtensionException(f'No {ext_path} extension found')

            if hasattr(obj, 'init_app') and callable(obj.init_app):
                obj.init_app(self.app)
            elif callable(obj):
                obj(self.app)
            else:
                raise NoExtensionException(
                    f'{ext_path} extension has no init_app.'
                )

            ext_name = ext_path.split('.')[-1]
            if ext_name not in self.app.extensions:
                self.app.extensions[ext_name] = obj

    def __register_blueprints(self):
        for blueprint_path in self.app.config.get('BLUEPRINTS', []):
            try:
                obj = import_object(blueprint_path)
                self.app.register_blueprint(obj)

            except ImportError:
                raise NoExtensionException(
                    f'No {blueprint_path} blueprint found'
                )


def create_app():
    app = AppFactory().app

    @app.before_request
    def before_request():
        if app.config['DEBUG']:
            g.start = time.time()

        get_resp_format()

    @app.after_request
    def after_request(response):
        if app.config['DEBUG']:
            diff = time.time() - g.start
            app.logger.debug(f'Request finished in {diff}')

        return response

    @app.teardown_request
    def teardown_request(exception):
        if exception:
            db.session.rollback()
        else:
            db.session.commit()

        db.session.remove()

    def app_error_response(error, status, default_text):
        db.session.rollback()

        errors_text = '; '.join(error.args) if error.args else default_text

        if not app.config['DEBUG'] and not isinstance(error, AppException):
            errors_text = default_text

        if status == 500:
            app.logger.error(errors_text, exc_info=True)

        data = {
            'error': {
                'code': get_subsonic_error_code(status),
                'message': errors_text
            }
        }

        return make_response(data, status)

    @app.errorhandler(Exception)
    def error_handler(error):
        if isinstance(error, (BadRequestError, AppValueError, ModelKeyError,)):
            return app_error_response(error, 400, 'Bad request')

        if isinstance(error, UnauthorizedError):
            return app_error_response(error, 401, 'Unauthorized')

        if isinstance(error, AccessDeniedError):
            return app_error_response(error, 403, 'Access denied')

        if isinstance(error, NotFoundError):
            return app_error_response(error, 404, 'Not found')

        if isinstance(error, HTTPException):
            return app_error_response(error, error.code, error.name)

        return app_error_response(error, 500, 'Unknown error')

    if app.config['DEBUG_SQL']:
        # noinspection PyUnusedLocal
        @event.listens_for(Engine, 'before_cursor_execute')
        def before_cursor_execute(conn, cursor, statement, parameters, context,
                                  executemany):
            conn.info.setdefault('query_start_time', []).append(time.time())
            app.logger.debug(f'Start Query: {statement}. '
                             f'With parameters: {parameters}')

        # noinspection PyUnusedLocal
        @event.listens_for(Engine, 'after_cursor_execute')
        def after_cursor_execute(conn, cursor, statement, parameters, context,
                                 executemany):
            total = time.time() - conn.info['query_start_time'].pop(-1)
            app.logger.debug(f'Query Complete. Total Time: {str(total)}\n')

    return app
