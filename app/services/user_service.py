import logging

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
)
from flask_smorest import abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy import asc

from app.db import db
from app.models.blocklist_model import BlocklistModel
from app.models.user_model import UserModel
from app.models.user_profile_model import UserProfileModel

# Create logger for this module
logger = logging.getLogger(__name__)


def get_all_user():
    users = UserModel.query.order_by(asc(UserModel.id)).all()

    results = []
    for user in users:
        # Create user info dict
        user_info = {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }
        results.append(user_info)

    return results


def get_user(user_id):
    user = UserModel.query.filter(UserModel.id == user_id).first()

    if not user:
        return None


    # Return user info with additional fields
    user_info = {
        "id": str(user.id),
        "email": user.email,
        "name": user.name,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }

    return user_info


def update_user(user_data, user_id):
    user = UserModel.query.filter(UserModel.id == user_id).first()
    if not user:
        logger.error("User doesn't exist, cannot update!")
        abort(400, message="User doesn't exist, cannot update!")

    try:
        if user_data.get("email"):
            user.email = user_data["email"]

        if user_data.get("name"):
            user.name = user_data["name"]

        if user_data.get("password"):
            # Hash password
            password = pbkdf2_sha256.hash(user_data["password"])
            user.password = password

        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        logger.error(f"Can not update! Error: {ex}")
        abort(400, message=f"Can not update! Error: {ex}")

    return {"message": "Update successfully!"}


def update_block_user(user_data, user_id):
    # Only admin can delete user
    jwt = get_jwt()
    if not jwt.get("is_admin"):
        logger.error("Admin privilege requierd.")
        abort(401, message="Admin privilege requierd.")

    if user_id == 1:
        logger.error("Can not block Super Admin!")
        abort(401, message="Can not block Super Admin!")

    user = UserModel.query.filter(UserModel.id == user_id, UserModel.deleted_at.is_(None)).first()

    if not user:
        logger.error("User doesn't exist, cannot update!")
        abort(400, message="User doesn't exist, cannot update!")

    try:
        # Update status block
        user.block = user_data["block"]

        db.session.add(user)
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        logger.error(f"Can not update status block User! Error: {ex}")
        abort(400, message=f"Can not update status block User! Error: {ex}")

    return {"message": "Block successfully!"}


def delete_user(id):
    # Only admin can delete user
    jwt = get_jwt()
    if not jwt.get("is_admin"):
        logger.error("Admin privilege requierd.")
        abort(401, message="Admin privilege requierd.")

    result = UserModel.query.filter_by(id=id).delete()
    if not result:
        logger.error("User doesn't exist, cannot delete!")
        abort(400, message="User doesn't exist, cannot delete!")

    db.session.commit()
    return {"message": "Delete successfully!"}


def login_user(user_data):
    # Check user by email with joined user_profile
    user = UserModel.query.filter(UserModel.email == user_data["email"]).first()

    # Verify
    if user and pbkdf2_sha256.verify(user_data["password"], user.password):
        # Create access_token - identity is user ID
        access_token = create_access_token(identity=user.id, fresh=True)

        # Create refresh_token
        refresh_token = create_refresh_token(identity=user.id)

        logger.info(f"User login successfully! email: {user_data['email']}")

        # Get user profile information
        profile = user.user_profile

        # Return user info with profile data (without password)
        user_info = {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "profile": {
                "age": profile.age if profile else None,
                "gender": profile.gender.value if profile and profile.gender else None,
                "height_cm": profile.height_cm if profile else None,
                "weight_kg": profile.weight_kg if profile else None,
                "activity_level": profile.activity_level.value if profile and profile.activity_level else None,
                "updated_at": profile.updated_at.isoformat() if profile and profile.updated_at else None
            } if profile else None
        }

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user_info
        }

    logger.error("Invalid credentials.")
    abort(400, message="Invalid credentials.")


def register_user(user_data):
    email = user_data["email"]
    password = user_data["password"]
    name = user_data.get("name")

    # Check email exist
    user = UserModel.query.filter(UserModel.email == email).first()
    if user:
        logger.error("Email already exists.")
        abort(400, message="Email already exists.")

    # Hash password
    password = pbkdf2_sha256.hash(password)

    new_user = UserModel(email=email, password=password, name=name)

    try:
        db.session.add(new_user)
        db.session.commit()

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Can not register! Error: {ex}")
        abort(400, message=f"Can not register! Error: {ex}")

    return {"message": "Register successfully!"}


def refresh_token():
    # Get id current user
    current_user_id = get_jwt_identity()

    # Create access_token
    access_token = create_access_token(identity=current_user_id, fresh=True)

    # Create refresh_token
    refresh_token = create_refresh_token(identity=current_user_id)

    # Block previous access_token
    jti = get_jwt()["jti"]

    # Block access token
    add_jti_blocklist(jti)

    return {"access_token": access_token, "refresh_token": refresh_token}


def get_current_user():
    """
    Get current user information from JWT token
    """
    # Get user ID from JWT token
    current_user_id = get_jwt_identity()

    # Query user from database with joined profile
    user = UserModel.query.filter(UserModel.id == current_user_id).first()

    if not user:
        logger.error("User not found!")
        abort(404, message="User not found!")

    # Get user profile information
    profile = user.user_profile

    # Return user info with profile data (without password)
    user_info = {
        "id": str(user.id),
        "email": user.email,
        "name": user.name,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "role": user.role,
        "profile": {
            "age": profile.age if profile else None,
            "gender": profile.gender.value if profile and profile.gender else None,
            "height_cm": profile.height_cm if profile else None,
            "weight_kg": profile.weight_kg if profile else None,
            "activity_level": profile.activity_level.value if profile and profile.activity_level else None,
            "updated_at": profile.updated_at.isoformat() if profile and profile.updated_at else None
        } if profile else None
    }

    return user_info



def add_jti_blocklist(jti):
    # Add to blockist when remove jti
    new_row = BlocklistModel(jti_blocklist=str(jti))

    try:
        db.session.add(new_row)
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        logger.error(f"Can not add jti! Error: {ex}")
        abort(400, message=f"Can not add jti! Error: {ex}")
