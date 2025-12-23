from flask.views import MethodView
from flask_smorest import Blueprint

from app.schemas.food_schema import (
    FoodCreateSchema,
    FoodResponseSchema,
    FoodUpdateSchema
)
from app.services import food_service

blp = Blueprint("Food", __name__, description="Food API")


@blp.route("/foods")
class FoodList(MethodView):
    @blp.response(200, FoodResponseSchema(many=True))
    def get(self):
        """Get all foods"""
        is_vietnamese = self.request.args.get('is_vietnamese', type=bool)
        result = food_service.get_all_foods(is_vietnamese=is_vietnamese)
        return result

    @blp.arguments(FoodCreateSchema)
    @blp.response(201, FoodResponseSchema)
    def post(self, food_data):
        """Create a new food"""
        result = food_service.create_food(food_data)
        return result


@blp.route("/foods/<food_id>")
class Food(MethodView):
    @blp.response(200, FoodResponseSchema)
    def get(self, food_id):
        """Get food by ID"""
        result = food_service.get_food(food_id)
        return result

    @blp.arguments(FoodUpdateSchema)
    @blp.response(200, FoodResponseSchema)
    def put(self, food_data, food_id):
        """Update food by ID"""
        result = food_service.update_food(food_id, food_data)
        return result

    @blp.response(200)
    def delete(self, food_id):
        """Delete food by ID"""
        result = food_service.delete_food(food_id)
        return result
