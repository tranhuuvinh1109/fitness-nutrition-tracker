from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.schemas.food_log_schema import (
    FoodLogCreateSchema,
    FoodLogResponseSchema,
    FoodLogUpdateSchema,
    FoodLogWithFoodSchema
)
from app.services import food_log_service

blp = Blueprint("FoodLog", __name__, description="Food Log API")


@blp.route("/food-logs")
class FoodLogList(MethodView):
    @jwt_required()
    @blp.response(200, FoodLogWithFoodSchema(many=True))
    def get(self):
        """Get all food logs for current user. Can filter by log_date or date range (start_day, end_day)"""
        from flask_jwt_extended import get_jwt_identity
        from flask import request
        user_id = get_jwt_identity()

        log_date = request.args.get('log_date')
        start_day = request.args.get('start_day')
        end_day = request.args.get('end_day')
        
        result = food_log_service.get_all_food_logs(
            user_id=user_id, 
            log_date=log_date,
            start_day=start_day,
            end_day=end_day
        )
        return result

    @jwt_required()
    @blp.arguments(FoodLogCreateSchema)
    @blp.response(201, FoodLogResponseSchema)
    def post(self, food_log_data):
        """Create a new food log for current user"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()

        result = food_log_service.create_food_log(user_id, food_log_data)
        return result


@blp.route("/food-logs/<food_log_id>")
class FoodLog(MethodView):
    @jwt_required()
    @blp.response(200, FoodLogWithFoodSchema)
    def get(self, food_log_id):
        """Get food log by ID"""
        result = food_log_service.get_food_log(food_log_id)

        # Check if user owns this food log
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if str(result.user_id) != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        return result

    @jwt_required()
    @blp.arguments(FoodLogUpdateSchema)
    @blp.response(200, FoodLogResponseSchema)
    def put(self, food_log_data, food_log_id):
        """Update food log by ID"""
        food_log = food_log_service.get_food_log(food_log_id)

        # Check if user owns this food log
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if str(food_log.user_id) != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        result = food_log_service.update_food_log(food_log_id, food_log_data)
        return result

    @jwt_required()
    @blp.response(200)
    def delete(self, food_log_id):
        """Delete food log by ID"""
        food_log = food_log_service.get_food_log(food_log_id)

        # Check if user owns this food log
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if str(food_log.user_id) != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        result = food_log_service.delete_food_log(food_log_id)
        return result
