from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint, abort

from app.schemas.workout_schema import (
    WorkoutCreateSchema,
    WorkoutResponseSchema,
    WorkoutUpdateSchema,
    WorkoutWithLogsSchema
)
from app.services import workout_service

blp = Blueprint("Workout", __name__, description="Workout API")


@blp.route("/workouts")
class WorkoutList(MethodView):
    @jwt_required()
    def get(self):
        """Get all workouts. If start_day or end_day is provided, returns workouts with user's workout logs (requires authentication)"""
        workout_type = request.args.get('type')
        start_day = request.args.get('start_day')
        end_day = request.args.get('end_day')
        
        # If start_day or end_day is provided, require authentication and return workouts with logs
        if start_day or end_day:
            user_id = get_jwt_identity()
            result = workout_service.get_all_workouts_with_logs(
                user_id=user_id,
                workout_type=workout_type,
                start_day=start_day,
                end_day=end_day
            )
            # Return with WorkoutWithLogsSchema - manually serialize since we can't use decorator conditionally
            schema = WorkoutWithLogsSchema(many=True)
            return schema.dump(result)
        else:
            # Normal case - return workouts without logs
            result = workout_service.get_all_workouts(workout_type=workout_type)
            schema = WorkoutResponseSchema(many=True)
            return schema.dump(result)

    @blp.arguments(WorkoutCreateSchema)
    @blp.response(201, WorkoutResponseSchema)
    def post(self, workout_data):
        """Create a new workout"""
        result = workout_service.create_workout(workout_data)
        return result


@blp.route("/workouts/<workout_id>")
class Workout(MethodView):
    @blp.response(200, WorkoutResponseSchema)
    def get(self, workout_id):
        """Get workout by ID"""
        result = workout_service.get_workout(workout_id)
        return result

    @blp.arguments(WorkoutUpdateSchema)
    @blp.response(200, WorkoutResponseSchema)
    def put(self, workout_data, workout_id):
        """Update workout by ID"""
        result = workout_service.update_workout(workout_id, workout_data)
        return result

    @blp.response(200)
    def delete(self, workout_id):
        """Delete workout by ID"""
        result = workout_service.delete_workout(workout_id)
        return result
