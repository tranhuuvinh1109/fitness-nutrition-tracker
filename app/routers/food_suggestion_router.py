from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.schemas.food_suggestion_schema import FoodSuggestionResponseSchema, FoodSuggestionRequestSchema
from app.services import food_suggestion_service

blp = Blueprint("FoodSuggestion", __name__, description="Food Suggestion API")


@blp.route("/food-suggestions")
class FoodSuggestion(MethodView):
    @jwt_required()
    @blp.arguments(FoodSuggestionRequestSchema)
    @blp.response(200, FoodSuggestionResponseSchema)
    def post(self, food_suggestion_data):
        """Generate a personalized food plan for the current user using AI"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()

        day_plan = food_suggestion_data.get("dayPlan")
        meal_type = food_suggestion_data.get("meal_type")
        result = food_suggestion_service.suggest_food_plan(user_id, day_plan, meal_type)
        return result
