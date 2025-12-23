from app.models.chat_message_model import ChatMessageModel as ChatMessage
from app.db import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class ChatService:
    def get_all_messages_by_conversation(self, conversation_id):
        """Lấy tất cả tin nhắn trong 1 conversation"""
        return (
            ChatMessage.query
            .filter(ChatMessage.conversation_id == conversation_id, ChatMessage.deleted_at.is_(None))
            .order_by(ChatMessage.created_at.asc())
            .all()
        )

    def get_message(self, message_id):
        """Lấy 1 tin nhắn theo id"""
        message = ChatMessage.query.filter(ChatMessage.id == message_id, ChatMessage.deleted_at.is_(None)).first()
        if not message:
            raise ValueError(f"Message {message_id} không tồn tại")
        return message

    def create_message(self, data):
        """Tạo tin nhắn mới"""

        message = ChatMessage(
            conversation_id=data.get("conversation_id"),
            sender_id=data.get("sender_id"),
            message=data.get("message"),
            message_type=data.get("message_type", "text"),
            message_metadata=data.get("metadata"),
        )
        try:
            db.session.add(message)
            db.session.commit()
            return message
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def update_message(self, message_id, data):
        """Cập nhật tin nhắn"""
        message = self.get_message(message_id)
        # Map metadata từ API sang message_metadata trong model
        field_mapping = {
            "message": "message",
            "message_type": "message_type",
            "metadata": "message_metadata"
        }
        for api_field, model_field in field_mapping.items():
            if api_field in data:
                setattr(message, model_field, data[api_field])
        try:
            db.session.commit()
            return message
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def delete_message(self, message_id):
        """Xóa tin nhắn"""
        message = self.get_message(message_id)
        try:
            db.session.delete(message)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

chat_service = ChatService()
