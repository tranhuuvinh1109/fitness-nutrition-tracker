import logging
import os
import json
from flask_smorest import abort
from openai import OpenAI

from app.db import db
from app.models.ai_message_model import AIMessageModel
from app.models.conversation_model import ConversationModel
from app.models.enums import AIRoleEnum
from app.services import user_profile_service

# Create logger for this module
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai_client = None

def get_openai_client():
    """Initialize and return OpenAI client"""
    global openai_client
    if openai_client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            abort(500, message="OpenAI API key not configured")
        openai_client = OpenAI(api_key=api_key)
    return openai_client


def get_or_create_conversation(user_id):
    """
    Get the most recent conversation for a user or create a new one.
    """
    conversation = ConversationModel.query.filter_by(user_id=user_id).order_by(
        ConversationModel.created_at.desc()
    ).first()

    if not conversation:
        conversation = ConversationModel(user_id=user_id)
        db.session.add(conversation)
        db.session.flush()
        logger.info(f"Created new conversation for user {user_id}")
    
    return conversation


def ask_ai(user_id, message_text):
    """
    Save user message, get AI response using user profile context, and save AI message.
    """
    try:
        # 0. Get or create conversation
        conversation = get_or_create_conversation(user_id)

        # 1. Save user message
        user_message = AIMessageModel(
            user_id=user_id,
            conversation_id=conversation.id,
            role=AIRoleEnum.user,
            content=message_text
        )
        db.session.add(user_message)
        db.session.flush() 

        # 2. Get user profile for context
        user_profile = user_profile_service.get_user_profile(user_id)
        user_context = "Người dùng chưa có profile."
        if user_profile:
            user_context = f"""
            Thông tin người dùng:
            - Tuổi: {user_profile.age}
            - Giới tính: {user_profile.gender.value if user_profile.gender else 'N/A'}
            - Chiều cao: {user_profile.height_cm} cm
            - Cân nặng: {user_profile.weight_kg} kg
            - BMI: {user_profile.bmi}
            - Mức độ hoạt động: {user_profile.activity_level.value if user_profile.activity_level else 'N/A'}
            - Mục tiêu: {json.dumps(user_profile.target, ensure_ascii=False) if user_profile.target else 'Không có'}
            """

        # 3. Call OpenAI
        client = get_openai_client()
        system_prompt = f"""Bạn là một chuyên gia tư vấn sức khỏe và dinh dưỡng cá nhân. 
        Dưới đây là hồ sơ của người dùng bạn đang trò chuyện cùng:
        {user_context}
        
        Hãy trả lời các câu hỏi của người dùng một cách chuyên nghiệp, hữu ích và dựa trên thông tin cá nhân của họ nếu có thể."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message_text}
            ],
            temperature=0.7
        )

        ai_content = response.choices[0].message.content

        # 4. Save AI response
        ai_message = AIMessageModel(
            user_id=user_id,
            conversation_id=conversation.id,
            role=AIRoleEnum.ai,
            content=ai_content
        )
        db.session.add(ai_message)
        db.session.commit()

        logger.info(f"AI response generated and saved for user {user_id}")
        return ai_message

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to ask AI: {ex}")
        abort(500, message=f"Failed to get AI response: {str(ex)}")

def get_all_ai_messages(user_id=None):
    """
    Get all AI messages. If user_id is provided, find messages belonging to the user's conversations.
    """
    if user_id:
        # Find all conversations for this user
        conversations = ConversationModel.query.filter_by(user_id=user_id).all()
        conversation_ids = [c.id for c in conversations]
        
        # Find all messages linked to these conversations
        return AIMessageModel.query.filter(
            AIMessageModel.conversation_id.in_(conversation_ids)
        ).order_by(AIMessageModel.created_at).all()
    
    # Otherwise return all messages (for admin/testing)
    return AIMessageModel.query.order_by(AIMessageModel.created_at).all()


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
