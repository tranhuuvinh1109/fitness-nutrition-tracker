from datetime import datetime
from app.db import db

class BlogModel(db.Model):
    __tablename__ = "blogs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)

    # NEW: Image URL
    image_url =  db.Column(db.Text, nullable=False)

    # Optional: short summary
    summary = db.Column(db.String(500), nullable=True)

    # Dates & metadata (if you want to use them)
    issued_date = db.Column(db.Date, nullable=True)        # Ban hành
    effective_date = db.Column(db.Date, nullable=True)     # Áp dụng
    updated_date = db.Column(db.Date, nullable=True)       # Cập nhật
    is_active = db.Column(db.Boolean, default=True)        # Hiệu lực

    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Blog {self.title}>"
