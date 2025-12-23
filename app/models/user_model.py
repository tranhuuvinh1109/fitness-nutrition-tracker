from datetime import datetime

from app.db import db


class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.Integer, default=2)  # 1: admin, 2: user, 3: guest
    block = db.Column(db.Boolean, default=False)
    balance = db.Column(db.Float, default=0.0)  # Số dư tài khoản
    time_created = db.Column(db.String(), default=datetime.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
