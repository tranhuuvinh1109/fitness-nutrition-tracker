import logging

from flask_smorest import abort

from app.db import db
from app.models.ai_message_model import AIMessageModel

# Create logger for this module
logger = logging.getLogger(__name__)


def get_all_ai_messages(user_id=None, role=None):
    """
    Get all AI messages, optionally filtered by user_id and/or role
    """
    query = AIMessageModel.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    if role:
        query = query.filter_by(role=role)

    ai_messages = query.order_by(AIMessageModel.created_at).all()
    return ai_messages


def get_ai_message(ai_message_id):
    """
    Get AI message by id
    """
    ai_message = AIMessageModel.query.filter_by(id=ai_message_id).first()

    if not ai_message:
        logger.error(f"AI message not found with id: {ai_message_id}")
        abort(404, message="AI message not found")

    return ai_message


def create_ai_message(user_id, ai_message_data):
    """
    Create a new AI message
    """
    try:
        ai_message = AIMessageModel(
            user_id=user_id,
            role=ai_message_data["role"],
            content=ai_message_data["content"]
        )

        db.session.add(ai_message)
        db.session.commit()

        logger.info(f"AI message created successfully with id: {ai_message.id}")
        return ai_message

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to create AI message: {ex}")
        abort(400, message=f"Failed to create AI message: {ex}")


def update_ai_message(ai_message_id, ai_message_data):
    """
    Update AI message
    """
    ai_message = AIMessageModel.query.filter_by(id=ai_message_id).first()

    if not ai_message:
        logger.error(f"AI message not found with id: {ai_message_id}")
        abort(404, message="AI message not found")

    try:
        if "role" in ai_message_data:
            ai_message.role = ai_message_data["role"]
        if "content" in ai_message_data:
            ai_message.content = ai_message_data["content"]

        db.session.commit()

        logger.info(f"AI message updated successfully with id: {ai_message_id}")
        return ai_message

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to update AI message: {ex}")
        abort(400, message=f"Failed to update AI message: {ex}")


def delete_ai_message(ai_message_id):
    """
    Delete AI message
    """
    ai_message = AIMessageModel.query.filter_by(id=ai_message_id).first()

    if not ai_message:
        logger.error(f"AI message not found with id: {ai_message_id}")
        abort(404, message="AI message not found")

    try:
        db.session.delete(ai_message)
        db.session.commit()

        logger.info(f"AI message deleted successfully with id: {ai_message_id}")
        return {"message": "AI message deleted successfully"}

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to delete AI message: {ex}")
        abort(400, message=f"Failed to delete AI message: {ex}")


def get_conversation_history(user_id, limit=50):
    """
    Get recent conversation history for a user
    """
    ai_messages = AIMessageModel.query.filter_by(user_id=user_id).order_by(
        AIMessageModel.created_at.desc()
    ).limit(limit).all()

    # Reverse to get chronological order (oldest first)
    return list(reversed(ai_messages))


def delete_conversation_history(user_id):
    """
    Delete all AI messages for a user
    """
    try:
        deleted_count = AIMessageModel.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        logger.info(f"Deleted {deleted_count} AI messages for user {user_id}")
        return {"message": f"Deleted {deleted_count} AI messages"}

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to delete conversation history: {ex}")
        abort(400, message=f"Failed to delete conversation history: {ex}")
