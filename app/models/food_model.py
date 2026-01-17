from uuid import uuid4

from app.db import db


class FoodModel(db.Model):
    __tablename__ = "foods"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(255), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
