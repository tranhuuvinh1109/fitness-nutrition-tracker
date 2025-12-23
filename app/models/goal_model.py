from datetime import datetime
from uuid import uuid4

from app.db import db
from app.models.enums import GoalTypeEnum


class GoalModel(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    goal_type = db.Column(db.Enum(GoalTypeEnum), nullable=False)
    target_weight = db.Column(db.Float)
    daily_calorie_target = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    user = db.relationship("UserModel", back_populates="goals")
