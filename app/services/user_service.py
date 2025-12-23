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
from app.models.ai_usage_model import AIUsageModel
from app.models.blocklist_model import BlocklistModel
from app.models.transaction_model import TransactionModel
from app.models.user_model import UserModel

# Create logger for this module
logger = logging.getLogger(__name__)


def get_user_total_used_amount(user_id):
    """
    Calculate total amount used by user from AI usage costs
    """
    from sqlalchemy import func
    result = db.session.query(func.sum(AIUsageModel.cost)).filter(
        AIUsageModel.user_id == user_id
    ).scalar()

    return result if result else 0.0


def get_user_total_deposited_amount(user_id):
    """
    Calculate total amount deposited by user from completed transactions (status=1)
    """
    from sqlalchemy import func
    result = db.session.query(func.sum(TransactionModel.amount)).filter(
        TransactionModel.user_id == user_id,
        TransactionModel.status == 1  # completed transactions
    ).scalar()

    return result if result else 0.0


def get_all_user():
    users = UserModel.query.filter(UserModel.deleted_at.is_(None)).order_by(asc(UserModel.id)).all()

    results = []
    for user in users:
        # Calculate additional amounts
        total_used_amount = get_user_total_used_amount(user.id)
        total_deposited_amount = get_user_total_deposited_amount(user.id)

        # Create user info dict
        user_info = {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "block": user.block,
            "time_created": user.time_created,
            "balance": user.balance,
            "total_used_amount": total_used_amount,
            "total_deposited_amount": total_deposited_amount
        }
        results.append(user_info)

    return results


def get_user(user_id):
    user = UserModel.query.filter(UserModel.id == user_id, UserModel.deleted_at.is_(None)).first()

    if not user:
        return None

    # Calculate additional amounts
    total_used_amount = get_user_total_used_amount(user.id)
    total_deposited_amount = get_user_total_deposited_amount(user.id)

    # Return user info with additional fields
    user_info = {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "block": user.block,
        "time_created": user.time_created,
        "balance": user.balance,
        "total_used_amount": total_used_amount,
        "total_deposited_amount": total_deposited_amount
    }

    return user_info


def update_user(user_data, user_id):
    user = UserModel.query.filter(UserModel.id == user_id, UserModel.deleted_at.is_(None)).first()
    if not user:
        logger.error("User doesn't exist, cannot update!")
        abort(400, message="User doesn't exist, cannot update!")

    try:
        if user_data["username"]:
            user.username = user_data["username"]

        if user_data["password"]:
            # Hash password
            password = pbkdf2_sha256.hash(user_data["password"])
            user.password = password

        # Update role if provided
        if "role" in user_data and user_data["role"]:
            user.role = user_data["role"]

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
    # Check user by email
    user = UserModel.query.filter(UserModel.email == user_data["email"], UserModel.deleted_at.is_(None)).first()

    # Verify
    if user and pbkdf2_sha256.verify(user_data["password"], user.password):
        # Create access_token - identity is user ID
        access_token = create_access_token(identity=user.id, fresh=True)

        # Create refresh_token
        refresh_token = create_refresh_token(identity=user.id)

        logger.info(f"User login successfully! email: {user_data['email']}")

        # Calculate additional amounts
        total_used_amount = get_user_total_used_amount(user.id)
        total_deposited_amount = get_user_total_deposited_amount(user.id)

        # Return user info without password
        user_info = {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "block": user.block,
            "time_created": user.time_created,
            "balance": user.balance,
            "total_used_amount": total_used_amount,
            "total_deposited_amount": total_deposited_amount
        }

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user_info
        }

    logger.error("Invalid credentials.")
    abort(400, message="Invalid credentials.")


def register_user(user_data):
    username = user_data["username"]
    email = user_data["email"]
    password = user_data["password"]

    # Check user name exist
    user = UserModel.query.filter(UserModel.username == user_data["username"], UserModel.deleted_at.is_(None)).first()
    if user:
        logger.error("Username already exists.")
        abort(400, message="Username already exists.")

    # Check email exist
    user = UserModel.query.filter(UserModel.email == email, UserModel.deleted_at.is_(None)).first()
    if user:
        logger.error("Email already exists.")
        abort(400, message="Email already exists.")

    # Hash password
    password = pbkdf2_sha256.hash(password)

    new_user = UserModel(username=username, email=email, password=password)

    try:
        db.session.add(new_user)
        db.session.commit()

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Can not register! Error: {ex}")
        abort(400, message=f"Can not register! Error: {ex}")

    # Default role is already set in UserModel (role=2 for regular user)

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
    
    # Query user from database
    user = UserModel.query.filter(UserModel.id == current_user_id, UserModel.deleted_at.is_(None)).first()
    
    if not user:
        logger.error("User not found!")
        abort(404, message="User not found!")

    # Calculate additional amounts
    total_used_amount = get_user_total_used_amount(user.id)
    total_deposited_amount = get_user_total_deposited_amount(user.id)

    # Return user info without password
    user_info = {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "block": user.block,
        "time_created": user.time_created,
        "balance": user.balance,
        "total_used_amount": total_used_amount,
        "total_deposited_amount": total_deposited_amount
    }

    return user_info


def upgrade_guest(guest_data):
    """
    Upgrade a guest (role=3) to a regular user (role=2)
    Requires email and password verification, and new username
    """
    email = guest_data["email"]
    username = guest_data["username"]
    password = guest_data["password"]

    # Find user by email
    user = UserModel.query.filter(UserModel.email == email, UserModel.deleted_at.is_(None)).first()
    if not user:
        logger.error(f"User with email {email} not found")
        abort(404, message="User not found")

    # Check if user is a guest (role = 3)
    if user.role != 3:
        logger.error(f"User {email} is not a guest (current role: {user.role})")
        abort(400, message="Only guest accounts can be upgraded")

    # Check if new username already exists (excluding current user)
    existing_user = UserModel.query.filter(
        UserModel.username == username,
        UserModel.id != user.id,
        UserModel.deleted_at.is_(None)
    ).first()
    if existing_user:
        logger.error(f"Username {username} already exists")
        abort(400, message="Username already exists")

    # Verify password
    if not pbkdf2_sha256.verify(password, user.password):
        logger.error(f"Invalid password for guest {email}")
        abort(401, message="Invalid password")

    try:
        # Update username and upgrade role from guest (3) to user (2)
        user.username = username
        user.role = 2
        db.session.commit()

        logger.info(f"Successfully upgraded guest {email} to user with username {username}")

        # Return user info after upgrade
        total_used_amount = get_user_total_used_amount(user.id)
        total_deposited_amount = get_user_total_deposited_amount(user.id)

        user_info = {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "block": user.block,
            "time_created": user.time_created,
            "balance": user.balance,
            "total_used_amount": total_used_amount,
            "total_deposited_amount": total_deposited_amount
        }

        return {
            "message": f"Guest upgraded to user successfully with username: {username}",
            "user": user_info
        }

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to upgrade guest {email}: {ex}")
        abort(500, message=f"Failed to upgrade guest: {ex}")


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
