from flask import Flask

from mvmusic import settings
from mvmusic.api.bp import bp


def create_app():
    app = Flask("mvmusic")
    app.config.from_object(settings)

    app.register_blueprint(bp)

    return app
