from datetime import datetime

from app.db import db


class ProcedureModel(db.Model):
    __tablename__ = "procedures"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    process_time = db.Column(db.Text, nullable=True)  # Thời gian xử lý
    authority_level = db.Column(db.Text, nullable=True)  # Cấp xử lý
    fee_text = db.Column(db.Text, nullable=True)  # Lệ phí
    process_steps = db.Column(db.JSON, nullable=True)  # Quy trình thực hiện
    required_documents = db.Column(db.JSON, nullable=True)  # Hồ sơ cần thiết
    important_notes = db.Column(db.JSON, nullable=True)  # Lưu ý quan trọng
    creator = db.Column(db.String(100), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # 👇 Soft delete
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Procedure {self.title}>"
