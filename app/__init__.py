import os

from flask import Flask
from app.blueprint import register_routing
from app.db import db
from app.extention import cors, migrate, scheduler
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
    
    # Initialize Scheduler
    scheduler.init_app(app)
    scheduler.start()
    
    # Add Cron Job
    from app.services.cron_service import send_daily_report
    # Avoid adding duplicate jobs in debug reloader
    if not scheduler.get_job("daily_email_job"):
        scheduler.add_job(
            id="daily_email_job",
            func=send_daily_report,
            trigger="cron",
            hour=13,
            minute=0
        )

    cors.init_app(app, supports_credentials=True, resources={r"*": {"origins": "*"}})
    manage.init_app(app)

    configure_logging(app)
    register_routing(app)

    return app


settings_module = os.getenv("APP_SETTINGS_MODULE")
app = create_app(settings_module)
