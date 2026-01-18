from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.schemas.workout_log_schema import (
    WorkoutLogCreateSchema,
    WorkoutLogResponseSchema,
    WorkoutLogUpdateSchema,
    WorkoutLogStatusUpdateBodySchema
)
from app.services import workout_log_service

blp = Blueprint("WorkoutLog", __name__, description="Workout Log API")


@blp.route("/workout-logs")
class WorkoutLogList(MethodView):
    @jwt_required()
    @blp.response(200, WorkoutLogResponseSchema(many=True))
    def get(self):
        """Get all workout logs for current user. Can filter by log_date or date range (start_day, end_day)"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()

        log_date = request.args.get('log_date')
        start_day = request.args.get('start_day')
        end_day = request.args.get('end_day')
        
        result = workout_log_service.get_all_workout_logs(
            user_id=user_id, 
            log_date=log_date,
            start_day=start_day,
            end_day=end_day
        )
        return result

    @jwt_required()
    @blp.arguments(WorkoutLogCreateSchema)
    @blp.response(201, WorkoutLogResponseSchema)
    def post(self, workout_log_data):
        """Create a new workout log for current user"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()

        result = workout_log_service.create_workout_log(user_id, workout_log_data)
        return result

    @jwt_required()
    @blp.arguments(WorkoutLogStatusUpdateBodySchema)
    @blp.response(200, WorkoutLogResponseSchema)
    def put(self, status_data):
        """Update workout log status for current user"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()
        
        workout_log_id = status_data["workout_log_id"]
        status = status_data["status"]
        
        # Get workout log and check ownership
        workout_log = workout_log_service.get_workout_log(workout_log_id)
        if str(workout_log.user_id) != user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")
            
        result = workout_log_service.update_workout_log(workout_log_id, {"status": status})
        return result


@blp.route("/workout-logs/<workout_log_id>")
class WorkoutLog(MethodView):
    @jwt_required()
    @blp.response(200, WorkoutLogResponseSchema)
    def get(self, workout_log_id):
        """Get workout log by ID"""
        result = workout_log_service.get_workout_log(workout_log_id)

        # Check if user owns this workout log
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if str(result.user_id) != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        return result

    @jwt_required()
    @blp.arguments(WorkoutLogUpdateSchema)
    @blp.response(200, WorkoutLogResponseSchema)
    def put(self, workout_log_data, workout_log_id):
        """Update workout log by ID"""
        workout_log = workout_log_service.get_workout_log(workout_log_id)

        # Check if user owns this workout log
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if str(workout_log.user_id) != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        result = workout_log_service.update_workout_log(workout_log_id, workout_log_data)
        return result

    @jwt_required()
    @blp.response(200)
    def delete(self, workout_log_id):
        """Delete workout log by ID"""
        workout_log = workout_log_service.get_workout_log(workout_log_id)

        # Check if user owns this workout log
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if str(workout_log.user_id) != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        result = workout_log_service.delete_workout_log(workout_log_id)
        return result
