from datetime import datetime

from app.db import db
from app.models.enums import GenderEnum, ActivityLevelEnum


class UserProfileModel(db.Model):
    __tablename__ = "user_profiles"

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), primary_key=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum(GenderEnum), nullable=True)
    height_cm = db.Column(db.Float)
    weight_kg = db.Column(db.Float)
    activity_level = db.Column(db.Enum(ActivityLevelEnum), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    bmi = db.Column(db.Float, nullable=True)
    target = db.Column(db.JSON, nullable=True)

    # Relationship
    user = db.relationship("UserModel", back_populates="user_profile")
