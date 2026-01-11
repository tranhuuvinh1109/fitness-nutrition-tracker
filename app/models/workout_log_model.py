from datetime import datetime, date
from uuid import uuid4

from app.db import db


class WorkoutLogModel(db.Model):
    __tablename__ = "workout_logs"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    workout_id = db.Column(db.String(36), db.ForeignKey("workouts.id"), nullable=False)
    duration_min = db.Column(db.Integer, nullable=False)
    calories_burned = db.Column(db.Integer)
    log_date = db.Column(db.Date, nullable=True)
    status = db.Column(
        db.Integer,
        default=0
    ) # 0: planned | 1: completed | 2: skipped
    note = db.Column(
        db.Text,
        nullable=True
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("UserModel", back_populates="workout_logs")
    workout = db.relationship("WorkoutModel", back_populates="workout_logs")
