from flask.views import MethodView
from flask_smorest import Blueprint

from app.schemas.blog_schema import BlogSchema, BlogCreateSchema, BlogUpdateSchema
from app.services.blog_service import blog_service

blp = Blueprint("Blog", __name__, description="Blog API")


@blp.route("/blogs")
class BlogList(MethodView):
    @blp.response(200, BlogSchema(many=True))
    def get(self):
        """Get all blogs"""
        return blog_service.get_all()

    @blp.arguments(BlogCreateSchema)
    @blp.response(201, BlogSchema)
    def post(self, blog_data):
        """Create a new blog"""
        return blog_service.create(blog_data)


@blp.route("/blogs/<int:blog_id>")
class Blog(MethodView):
    @blp.response(200, BlogSchema)
    def get(self, blog_id):
        """Get blog detail"""
        return blog_service.get(blog_id)

    @blp.arguments(BlogUpdateSchema)
    @blp.response(200, BlogSchema)
    def put(self, blog_data, blog_id):
        """Update a blog"""
        return blog_service.update(blog_id, blog_data)

    @blp.response(204)
    def delete(self, blog_id):
        """Delete a blog"""
        blog_service.delete(blog_id)
        return {}
