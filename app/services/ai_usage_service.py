import logging
from math import ceil

from flask_smorest import abort
from sqlalchemy import desc, and_

from app.db import db
from app.models.ai_usage_model import AIUsageModel
from app.models.user_model import UserModel

# Create logger for this module
logger = logging.getLogger(__name__)


def create_ai_usage(ai_usage_data):
    """Create a new AI usage record"""
    try:
        ai_usage = AIUsageModel(
            user_id=ai_usage_data["user_id"],
            conversation_id=ai_usage_data.get("conversation_id"),
            model=ai_usage_data["model"],
            tokens_used=ai_usage_data["tokens_used"],
            cost=ai_usage_data["cost"]
        )

        db.session.add(ai_usage)
        db.session.commit()

        logger.info(f"AI usage recorded for user {ai_usage_data['user_id']}")
        return ai_usage

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating AI usage record: {str(e)}")
        abort(500, message="Failed to record AI usage")


def get_user_ai_usage(user_id, filter_data=None):
    """Get AI usage history for a specific user"""
    query = AIUsageModel.query.filter(AIUsageModel.user_id == user_id, AIUsageModel.deleted_at.is_(None))

    if filter_data:
        if filter_data.get("model"):
            query = query.filter(AIUsageModel.model == filter_data["model"])
        if filter_data.get("conversation_id"):
            query = query.filter(AIUsageModel.conversation_id == filter_data["conversation_id"])

    # Pagination
    page = filter_data.get("page", 1) if filter_data else 1
    page_size = filter_data.get("page_size", 20) if filter_data else 20

    total_usage = query.count()
    total_page = ceil(total_usage / page_size)

    usages = query.order_by(desc(AIUsageModel.created_at)) \
                  .offset((page - 1) * page_size) \
                  .limit(page_size) \
                  .all()

    return {
        "results": usages,
        "total_page": total_page,
        "total_usage": total_usage
    }


def get_all_ai_usage(filter_data=None):
    """Get all AI usage records with optional filtering"""
    query = AIUsageModel.query

    if filter_data:
        if filter_data.get("user_id"):
            query = query.filter(AIUsageModel.user_id == filter_data["user_id"])
        if filter_data.get("model"):
            query = query.filter(AIUsageModel.model == filter_data["model"])
        if filter_data.get("conversation_id"):
            query = query.filter(AIUsageModel.conversation_id == filter_data["conversation_id"])

    # Pagination
    page = filter_data.get("page", 1) if filter_data else 1
    page_size = filter_data.get("page_size", 20) if filter_data else 20

    total_usage = query.count()
    total_page = ceil(total_usage / page_size)

    usages = query.order_by(desc(AIUsageModel.created_at)) \
                  .offset((page - 1) * page_size) \
                  .limit(page_size) \
                  .all()

    return {
        "results": usages,
        "total_page": total_page,
        "total_usage": total_usage
    }


def deduct_user_balance(user_id, amount=500):
    """Deduct amount from user balance and return the user"""
    user = UserModel.query.filter(UserModel.id == user_id, UserModel.deleted_at.is_(None)).first()
    if not user:
        abort(404, message="User not found")

    if user.balance < amount:
        abort(400, message="Insufficient balance")

    user.balance -= amount
    db.session.commit()

    logger.info(f"Deducted {amount} from user {user_id}, new balance: {user.balance}")
    return user


def get_user_total_cost(user_id):
    """Get total cost spent by user on AI"""
    result = db.session.query(db.func.sum(AIUsageModel.cost)).filter(
        AIUsageModel.user_id == user_id,
        AIUsageModel.deleted_at.is_(None)
    ).scalar()

    return result or 0.0


def get_usage_stats(user_id=None):
    """Get usage statistics"""
    if user_id:
        # User-specific stats
        total_cost = get_user_total_cost(user_id)
        usage_count = AIUsageModel.query.filter(AIUsageModel.user_id == user_id, AIUsageModel.deleted_at.is_(None)).count()
        user = UserModel.query.filter(UserModel.id == user_id, UserModel.deleted_at.is_(None)).first()

        return {
            "user_id": user_id,
            "total_cost": total_cost,
            "usage_count": usage_count,
            "current_balance": user.balance if user else 0.0
        }
    else:
        # Global stats
        total_cost = db.session.query(db.func.sum(AIUsageModel.cost)).filter(AIUsageModel.deleted_at.is_(None)).scalar() or 0.0
        usage_count = AIUsageModel.query.filter(AIUsageModel.deleted_at.is_(None)).count()
        total_users = AIUsageModel.query.filter(AIUsageModel.deleted_at.is_(None)).distinct(AIUsageModel.user_id).count()

        return {
            "total_cost": total_cost,
            "usage_count": usage_count,
            "total_users": total_users
        }
