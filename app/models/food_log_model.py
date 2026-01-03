from datetime import datetime, date
from uuid import uuid4
from app.models.enums import MealTypeEnum

from app.db import db


class FoodLogModel(db.Model):
    __tablename__ = "food_logs"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    food_id = db.Column(db.String(36), db.ForeignKey("foods.id"), nullable=False)
    quantity = db.Column(db.Float, default=1.0)
    log_date = db.Column(db.Date, nullable=False)
    meal_type = db.Column(db.Enum(MealTypeEnum), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("UserModel", back_populates="food_logs")
    food = db.relationship("FoodModel", back_populates="food_logs")
