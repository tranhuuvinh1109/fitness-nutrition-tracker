from uuid import uuid4

from app.db import db
from app.models.enums import WorkoutTypeEnum


class WorkoutModel(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum(WorkoutTypeEnum), nullable=False)

    # Relationships
    workout_logs = db.relationship("WorkoutLogModel", back_populates="workout", cascade="all, delete-orphan")
