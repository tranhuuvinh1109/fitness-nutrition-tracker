from datetime import datetime
from app.db import db

class ConversationModel(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.String(100), primary_key=True)  # UUID hoặc session ID
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    title = db.Column(db.String(255), nullable=True)  # Tiêu đề optional
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
