import logging
import uuid
from datetime import timedelta

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_smorest import abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy import or_

from app.db import db
from app.models.user_model import UserModel

# Create logger for this module
logger = logging.getLogger(__name__)

# Default password for guest users (hashed)
GUEST_PASSWORD = pbkdf2_sha256.hash("guest_password_123")


def create_guest_user():
    """
    Create a new guest user and return access token
    """
    try:
        # Generate unique ID for guest
        guest_id = str(uuid.uuid4())

        # Create guest username and email
        username = f"guest_{guest_id}"
        email = f"guest_{guest_id}@guest.local"

        # Create guest user in database
        guest_user = UserModel(
            username=username,
            email=email,
            password=GUEST_PASSWORD,
            role=3,  # 3: guest role
            block=False
        )

        db.session.add(guest_user)
        db.session.commit()

        # Create access token with user identity
        access_token = create_access_token(
            identity=guest_user.id,
            additional_claims={
                "user_type": "guest",
                "username": username
            },
            expires_delta=timedelta(hours=24)  # Token expires in 24 hours
        )

        logger.info(f"Guest user created successfully! Username: {username}")

        return {
            "access_token": access_token,
            "id": guest_user.id,
            "username": username,
            "email": email,
            "user_type": "guest",
            "expires_in": 86400,  # 24 hours in seconds
            "message": "Guest user created successfully",
            "role": 3
        }

    except Exception as e:
        logger.error(f"Error creating guest user: {str(e)}")
        db.session.rollback()
        raise e


def get_guest_user(user_id):
    """
    Get guest user by ID
    """
    try:
        user = UserModel.query.filter(UserModel.id == user_id, UserModel.role == 3, UserModel.deleted_at.is_(None)).first()  # role=3 for guests
        if not user:
            return None

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "block": user.block,
            "time_created": user.time_created,
            "user_type": "guest"
        }

    except Exception as e:
        logger.error(f"Error getting guest user: {str(e)}")
        raise e


def cleanup_guest_users():
    """
    Clean up old guest users (optional - for maintenance)
    This could be run periodically to remove old guest accounts
    """
    try:
        # This is just an example - you might want to implement time-based cleanup
        # For now, we'll skip this as guest users are meant to persist
        logger.info("Guest user cleanup skipped - guests are persistent")
        return 0

    except Exception as e:
        logger.error(f"Error cleaning up guest users: {str(e)}")
        raise e


def upgrade_guest_to_user(user_id, upgrade_data):
    """
    Upgrade a guest user to a regular user with new credentials

    Args:
        user_id (int): The guest user ID to upgrade
        upgrade_data (dict): Contains email, username, password

    Returns:
        dict: Login response with tokens and user data
    """
    try:
        # Get the user
        user = UserModel.query.filter(UserModel.id == user_id, UserModel.deleted_at.is_(None)).first()
        if not user:
            logger.error(f"User with id {user_id} not found")
            abort(404, message="User not found")

        # Check if user is a guest (role = 3)
        if user.role != 3:
            logger.error(f"User {user_id} is not a guest user (role: {user.role})")
            abort(400, message="User is not a guest and cannot be upgraded")

        # Validate new credentials
        email = upgrade_data.get("email", "").strip()
        username = upgrade_data.get("username", "").strip()
        password = upgrade_data.get("password", "").strip()

        if not email or not username or not password:
            abort(400, message="Email, username, and password are required")

        if len(password) < 6:
            abort(400, message="Password must be at least 6 characters long")

        # Check if email or username already exists
        existing_user = UserModel.query.filter(
            or_(UserModel.email == email, UserModel.username == username),
            UserModel.deleted_at.is_(None)
        ).first()

        if existing_user and existing_user.id != user_id:
            abort(400, message="Email or username already exists")

        # Update user information
        user.email = email
        user.username = username
        user.password = pbkdf2_sha256.hash(password)
        user.role = 2  # Change from guest (3) to regular user (2)

        db.session.commit()

        # Create new tokens for the upgraded user
        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                "user_type": "user",
                "username": username,
                "role": user.role
            }
        )

        refresh_token = create_refresh_token(identity=user.id)

        logger.info(f"Successfully upgraded guest user {user_id} to regular user")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "block": user.block,
                "balance": user.balance,
                "time_created": user.time_created
            }
        }

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error upgrading guest user {user_id}: {str(e)}")
        if hasattr(e, 'code'):  # Flask-Smorest abort exception
            raise e
        abort(500, message="Failed to upgrade guest user")

