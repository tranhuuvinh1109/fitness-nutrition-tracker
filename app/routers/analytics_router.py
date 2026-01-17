from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.schemas.analytics_schema import AnalyticsRequestSchema, AnalyticsItemSchema, AnalyticsWorkoutItemSchema
from app.services import analytics_service

blp = Blueprint("Analytics", __name__, description="Analytics API")

@blp.route("/analytics/calo")
class AnalyticsCalo(MethodView):
    @jwt_required()
    @blp.arguments(AnalyticsRequestSchema, location="query")
    @blp.response(200, AnalyticsItemSchema(many=True))
    def get(self, args):
        """Get calories and macros analytics data"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()
        
        mode = args.get("mode", 7)
        result = analytics_service.get_nutrition_analytics(user_id, mode)
        return result


@blp.route("/analytics/workout")
class AnalyticsWorkout(MethodView):
    @jwt_required()
    @blp.arguments(AnalyticsRequestSchema, location="query")
    @blp.response(200, AnalyticsWorkoutItemSchema(many=True))
    def get(self, args):
        """Get workout analytics data (duration, calories burned)"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()
        
        mode = args.get("mode", 7)
        result = analytics_service.get_workout_analytics(user_id, mode)
        return result
