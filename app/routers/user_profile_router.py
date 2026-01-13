from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from flask_jwt_extended import get_jwt_identity


from app.schemas.user_profile_schema import (
    UserProfileResponseSchema,
    UserProfileUpdateSchema
)
from app.services import user_profile_service

blp = Blueprint("UserProfile", __name__, description="User Profile API")


@blp.route("/user-profile")
class UserProfileList(MethodView):
    @jwt_required()
    @blp.response(200, UserProfileResponseSchema)
    def get(self):
        """Get current user's profile"""
        
        user_id = get_jwt_identity()

        result = user_profile_service.get_user_profile(user_id)
        if not result:
            from flask_smorest import abort
            abort(404, message="User profile not found")

        return result

    @jwt_required()
    @blp.arguments(UserProfileUpdateSchema)
    @blp.response(200, UserProfileResponseSchema)
    def put(self, profile_data):
        """Update current user's profile"""
        
        user_id = get_jwt_identity()

        result = user_profile_service.update_user_profile(user_id, profile_data)
        return result

    @jwt_required()
    @blp.response(200)
    def post(self):
        """Create profile for current user"""
        
        user_id = get_jwt_identity()

        # Create empty profile - will be updated via PUT
        result = user_profile_service.create_user_profile(user_id, {})
        return result


@blp.route("/user-profile/<user_profile_id>")
class UserProfile(MethodView):
    @jwt_required()
    @blp.response(200, UserProfileResponseSchema)
    def get(self, user_profile_id):
        """Get user profile by ID"""
        
        current_user_id = get_jwt_identity()

        # Users can only access their own profile
        if user_profile_id != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        result = user_profile_service.get_user_profile(user_profile_id)
        if not result:
            abort(404, message="User profile not found")

        return result

    @jwt_required()
    @blp.arguments(UserProfileUpdateSchema)
    @blp.response(200, UserProfileResponseSchema)
    def put(self, profile_data, user_profile_id):
        """Update user profile by ID"""
        
        current_user_id = get_jwt_identity()

        # Users can only update their own profile
        if user_profile_id != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        result = user_profile_service.update_user_profile(user_profile_id, profile_data)
        return result

    @jwt_required()
    @blp.response(200)
    def delete(self, user_profile_id):
        """Delete user profile by ID"""
        
        current_user_id = get_jwt_identity()

        # Users can only delete their own profile
        if user_profile_id != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        result = user_profile_service.delete_user_profile(user_profile_id)
        return result
