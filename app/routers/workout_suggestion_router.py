from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.schemas.workout_suggestion_schema import (
    WorkoutSuggestionResponseSchema,
    WorkoutSuggestionRequestSchema
)
from app.services import workout_suggestion_service

blp = Blueprint("WorkoutSuggestion", __name__, description="Workout Suggestion API")


@blp.route("/workout-suggestions")
class WorkoutSuggestion(MethodView):
    @jwt_required()
    @blp.arguments(WorkoutSuggestionRequestSchema)
    @blp.response(200, WorkoutSuggestionResponseSchema)
    def post(self, suggestion_data):
        """Generate a personalized workout plan for the current user using AI"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()

        start_day = suggestion_data.get('start_day')
        end_day = suggestion_data.get('end_day')

        result = workout_suggestion_service.suggest_workout_plan(user_id, start_day, end_day)
        return result
