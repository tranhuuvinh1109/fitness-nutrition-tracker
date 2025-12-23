from flask.views import MethodView
from flask_smorest import Blueprint

from app.schemas.workout_schema import (
    WorkoutCreateSchema,
    WorkoutResponseSchema,
    WorkoutUpdateSchema
)
from app.services import workout_service

blp = Blueprint("Workout", __name__, description="Workout API")


@blp.route("/workouts")
class WorkoutList(MethodView):
    @blp.response(200, WorkoutResponseSchema(many=True))
    def get(self):
        """Get all workouts"""
        workout_type = self.request.args.get('type')
        result = workout_service.get_all_workouts(workout_type=workout_type)
        return result

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
