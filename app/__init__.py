import os

from flask import Flask
from app.blueprint import register_routing
from app.db import db
from app.extention import cors, migrate
from app.utils.auth import jwt
from app.utils.logging import configure_logging
import manage


def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    cors.init_app(app, supports_credentials=True, resources={r"*": {"origins": "*"}})
    manage.init_app(app)

    configure_logging(app)
    register_routing(app)

    return app


settings_module = os.getenv("APP_SETTINGS_MODULE")
app = create_app(settings_module)
