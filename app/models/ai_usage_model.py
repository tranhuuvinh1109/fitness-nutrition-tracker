from datetime import datetime

from app.db import db


class AIUsageModel(db.Model):
    __tablename__ = "ai_usage"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    conversation_id = db.Column(db.String(100), db.ForeignKey("conversations.id"), nullable=True)
    model = db.Column(db.String(50), nullable=False)  # gpt-4, gpt-3.5-turbo, etc.
    tokens_used = db.Column(db.Integer, nullable=False)  # Số tokens đã sử dụng
    cost = db.Column(db.Float, nullable=False)  # Chi phí tính theo USD
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Relationship với User và Conversation
    user = db.relationship("UserModel", backref=db.backref("ai_usages", lazy=True))
    conversation = db.relationship("ConversationModel", backref=db.backref("ai_usages", lazy=True))
