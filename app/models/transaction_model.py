from datetime import datetime

from app.db import db


class TransactionModel(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.Integer, nullable=False)  # 0: pending, 1: completed, 2: failed, 3: cancelled
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # credit_card, bank_transfer, paypal, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    additional_data = db.Column(db.JSON, nullable=True)  # Additional data as JSON
    code = db.Column(db.String(12), nullable=True)  # Last part of UUID v4 (12 characters)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Relationship với User
    user = db.relationship("UserModel", backref=db.backref("transactions", lazy=True))
    
