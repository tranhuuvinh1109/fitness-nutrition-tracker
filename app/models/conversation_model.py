from datetime import datetime
from uuid import uuid4

from app.db import db


class ConversationModel(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("UserModel", back_populates="conversations")
    ai_messages = db.relationship("AIMessageModel", back_populates="conversation", cascade="all, delete-orphan")
