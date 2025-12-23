from app.models.blog_model import BlogModel as Blog
from app.db import db
from sqlalchemy.exc import SQLAlchemyError


class BlogService:
    def get_all(self):
        """Lấy tất cả blog"""
        return Blog.query.filter(Blog.deleted_at.is_(None)).order_by(Blog.created_at.desc()).all()

    def get(self, blog_id):
        """Lấy chi tiết blog theo id"""
        blog = Blog.query.filter(Blog.id == blog_id, Blog.deleted_at.is_(None)).first()
        if not blog:
            raise ValueError(f"Blog với id {blog_id} không tồn tại")
        return blog

    def create(self, data):
        """Tạo blog mới"""
        blog = Blog(
            title=data.get("title"),
            content=data.get("content"),
            author=data.get("author"),
            image_url=data.get("image_url"),
            summary=data.get("summary"),
            issued_date=data.get("issued_date"),
            effective_date=data.get("effective_date"),
            updated_date=data.get("updated_date"),
            is_active=data.get("is_active", True)
        )
        try:
            db.session.add(blog)
            db.session.commit()
            return blog
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def update(self, blog_id, data):
        """Cập nhật blog"""
        blog = Blog.query.filter(Blog.id == blog_id, Blog.deleted_at.is_(None)).first()
        if not blog:
            raise ValueError(f"Blog với id {blog_id} không tồn tại")

        # Cập nhật từng trường nếu có trong data
        for field in [
            "title", "content", "author", "image_url", "summary",
            "issued_date", "effective_date", "updated_date", "is_active"
        ]:
            if field in data:
                setattr(blog, field, data[field])

        try:
            db.session.commit()
            return blog
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def delete(self, blog_id):
        """Xóa blog"""
        blog = Blog.query.filter(Blog.id == blog_id, Blog.deleted_at.is_(None)).first()
        if not blog:
            raise ValueError(f"Blog với id {blog_id} không tồn tại")
        try:
            db.session.delete(blog)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e


# Khởi tạo service
blog_service = BlogService()
