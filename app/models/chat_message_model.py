from datetime import datetime
from app.db import db

class ChatMessageModel(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.String(100), nullable=False, index=True)  # ID của cuộc trò chuyện (có thể là session)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)  # Khóa phụ tới bảng User (None nếu là bot)
    message = db.Column(db.Text, nullable=False)  # Nội dung tin nhắn
    message_type = db.Column(db.String(20), default="text")  # text, image, audio, file...
    message_metadata = db.Column("metadata", db.JSON, nullable=True)  # Metadata dạng JSON (tên cột DB: metadata)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<ChatMessage sender_id={self.sender_id}: {self.message[:20]}>"
