from datetime import datetime, date
from uuid import uuid4

from app.db import db


class WaterLogModel(db.Model):
    __tablename__ = "water_logs"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    amount_ml = db.Column(db.Integer, nullable=False)
    log_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    user = db.relationship("UserModel", back_populates="water_logs")
