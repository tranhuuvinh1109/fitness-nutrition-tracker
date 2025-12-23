import logging
import time
from functools import wraps

from flask_jwt_extended import get_jwt
from flask_smorest import abort

from app.models import UserModel

# Create logger for this module
logger = logging.getLogger(__name__)


def permission_required(permission_name):
    """Simplified permission check - only checks if user is admin (role == 1)"""
    def decorator(func):
        def wrapper(*arg, **kwargs):
            jwt_data = get_jwt()
            is_admin = jwt_data.get("is_admin", False)
            if not is_admin:
                logger.error("Admin privilege required!")
                abort(403, message="Admin privilege required!")
            return func(*arg, **kwargs)

        return wrapper

    return decorator


def time_profiling(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Function {func.__name__} took {end_time-start_time:.4f}s.")
        return result

    return wrapper
