from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.schemas.user_schema import (
    UserLoginInputSchema,
    UserRegisterSchema,
    UserResponseSchema,
    UserGetCurrentSchema,
)
from app.services import user_service

blp = Blueprint("User", __name__, description="User API")


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserLoginInputSchema)
    def post(self, user_data):
        result = user_service.login_user(user_data)
        return result


@blp.route("/register")
class Register(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        result = user_service.register_user(user_data)
        return result


@blp.route("/me")
class Me(MethodView):
    @jwt_required()
    @blp.response(200, UserGetCurrentSchema)
    def get(self):
        """Get current user information from access token"""
        result = user_service.get_current_user()
        return result