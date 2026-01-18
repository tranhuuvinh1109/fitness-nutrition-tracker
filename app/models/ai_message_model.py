from datetime import datetime
from uuid import uuid4

from app.db import db
from app.models.enums import AIRoleEnum


class AIMessageModel(db.Model):
    __tablename__ = "ai_messages"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    conversation_id = db.Column(db.String(36), db.ForeignKey("conversations.id"), nullable=True) # Initially nullable for migration compatibility
    role = db.Column(db.Enum(AIRoleEnum), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    user = db.relationship("UserModel", back_populates="ai_messages")
    conversation = db.relationship("ConversationModel", back_populates="ai_messages")
