from datetime import datetime
from uuid import uuid4

from app.db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user_profile = db.relationship("UserProfileModel", back_populates="user", uselist=False, cascade="all, delete-orphan")
    goals = db.relationship("GoalModel", back_populates="user", cascade="all, delete-orphan")
    food_logs = db.relationship("FoodLogModel", back_populates="user", cascade="all, delete-orphan")
    workout_logs = db.relationship("WorkoutLogModel", back_populates="user", cascade="all, delete-orphan")
    water_logs = db.relationship("WaterLogModel", back_populates="user", cascade="all, delete-orphan")
    ai_messages = db.relationship("AIMessageModel", back_populates="user", cascade="all, delete-orphan")
