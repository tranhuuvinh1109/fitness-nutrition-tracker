import logging

from flask_smorest import abort

from app.db import db
from app.models.user_profile_model import UserProfileModel

# Create logger for this module
logger = logging.getLogger(__name__)


def get_user_profile(user_id):
    """
    Get user profile by user_id
    """
    profile = UserProfileModel.query.filter_by(user_id=user_id).first()

    if not profile:
        logger.error(f"User profile not found for user_id: {user_id}")
        return None

    return profile


def create_user_profile(user_id, profile_data):
    """
    Create a new user profile
    """
    # Check if profile already exists
    existing_profile = UserProfileModel.query.filter_by(user_id=user_id).first()
    if existing_profile:
        logger.error(f"User profile already exists for user_id: {user_id}")
        abort(400, message="User profile already exists")

    try:
        profile = UserProfileModel(
            user_id=user_id,
            age=profile_data.get("age"),
            gender=profile_data.get("gender"),
            height_cm=profile_data.get("height_cm"),
            weight_kg=profile_data.get("weight_kg"),
            activity_level=profile_data.get("activity_level")
        )

        db.session.add(profile)
        db.session.commit()

        logger.info(f"User profile created successfully for user_id: {user_id}")
        return profile

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to create user profile: {ex}")
        abort(400, message=f"Failed to create user profile: {ex}")


def update_user_profile(user_id, profile_data):
    """
    Update user profile
    """
    profile = UserProfileModel.query.filter_by(user_id=user_id).first()

    if not profile:
        logger.error(f"User profile not found for user_id: {user_id}")
        abort(404, message="User profile not found")

    try:
        if "age" in profile_data:
            profile.age = profile_data["age"]
        if "gender" in profile_data:
            profile.gender = profile_data["gender"]
        if "height_cm" in profile_data:
            profile.height_cm = profile_data["height_cm"]
        if "weight_kg" in profile_data:
            profile.weight_kg = profile_data["weight_kg"]
        if "activity_level" in profile_data:
            profile.activity_level = profile_data["activity_level"]

        db.session.commit()

        logger.info(f"User profile updated successfully for user_id: {user_id}")
        return profile

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to update user profile: {ex}")
        abort(400, message=f"Failed to update user profile: {ex}")


def delete_user_profile(user_id):
    """
    Delete user profile
    """
    profile = UserProfileModel.query.filter_by(user_id=user_id).first()

    if not profile:
        logger.error(f"User profile not found for user_id: {user_id}")
        abort(404, message="User profile not found")

    try:
        db.session.delete(profile)
        db.session.commit()

        logger.info(f"User profile deleted successfully for user_id: {user_id}")
        return {"message": "User profile deleted successfully"}

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to delete user profile: {ex}")
        abort(400, message=f"Failed to delete user profile: {ex}")
