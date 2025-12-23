from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.schemas.ai_usage_schema import AIUsagePageSchema, AIUsageStatsSchema
from app.services import ai_usage_service
from app.utils.decorators import permission_required

blp = Blueprint("AI Usage", __name__, description="AI Usage History API")


@blp.route("/ai-usage/user/<int:user_id>")
class UserAIUsage(MethodView):
    @jwt_required()
    @permission_required(permission_name="read")
    @blp.response(200, AIUsagePageSchema)
    def get(self, user_id):
        """Get AI usage history for a specific user"""
        result = ai_usage_service.get_user_ai_usage(user_id)
        return result


@blp.route("/ai-usage/user/<int:user_id>/stats")
class UserAIUsageStats(MethodView):
    @jwt_required()
    @permission_required(permission_name="read")
    @blp.response(200, AIUsageStatsSchema)
    def get(self, user_id):
        """Get AI usage statistics for a specific user"""
        result = ai_usage_service.get_usage_stats(user_id)
        return result


@blp.route("/ai-usage/stats")
class AIUsageStats(MethodView):
    @jwt_required()
    @permission_required(permission_name="read")
    @blp.response(200, AIUsageStatsSchema)
    def get(self):
        """Get global AI usage statistics"""
        result = ai_usage_service.get_usage_stats()
        return result


@blp.route("/ai-usage")
class AIUsageList(MethodView):
    @jwt_required()
    @permission_required(permission_name="read")
    @blp.response(200, AIUsagePageSchema)
    def get(self):
        """Get all AI usage records (admin only)"""
        result = ai_usage_service.get_all_ai_usage()
        return result
