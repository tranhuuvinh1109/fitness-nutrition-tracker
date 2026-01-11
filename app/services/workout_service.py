import logging
from datetime import datetime

from flask_smorest import abort

from app.db import db
from app.models.workout_model import WorkoutModel
from app.models.workout_log_model import WorkoutLogModel

# Create logger for this module
logger = logging.getLogger(__name__)


def get_all_workouts(workout_type=None):
    """
    Get all workouts, optionally filtered by type
    """
    query = WorkoutModel.query
    if workout_type:
        query = query.filter_by(type=workout_type)

    workouts = query.all()
    return workouts


def get_workout(workout_id):
    """
    Get workout by id
    """
    workout = WorkoutModel.query.filter_by(id=workout_id).first()

    if not workout:
        logger.error(f"Workout not found with id: {workout_id}")
        abort(404, message="Workout not found")

    return workout


def create_workout(workout_data):
    """
    Create a new workout
    """
    try:
        workout = WorkoutModel(
            name=workout_data["name"],
            type=workout_data["type"],
            met=workout_data.get("met")
        )

        db.session.add(workout)
        db.session.commit()

        logger.info(f"Workout created successfully with id: {workout.id}")
        return workout

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to create workout: {ex}")
        abort(400, message=f"Failed to create workout: {ex}")


def update_workout(workout_id, workout_data):
    """
    Update workout
    """
    workout = WorkoutModel.query.filter_by(id=workout_id).first()

    if not workout:
        logger.error(f"Workout not found with id: {workout_id}")
        abort(404, message="Workout not found")

    try:
        if "name" in workout_data:
            workout.name = workout_data["name"]
        if "type" in workout_data:
            workout.type = workout_data["type"]
        if "met" in workout_data:
            workout.met = workout_data["met"]

        db.session.commit()

        logger.info(f"Workout updated successfully with id: {workout_id}")
        return workout

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to update workout: {ex}")
        abort(400, message=f"Failed to update workout: {ex}")


def delete_workout(workout_id):
    """
    Delete workout
    """
    workout = WorkoutModel.query.filter_by(id=workout_id).first()

    if not workout:
        logger.error(f"Workout not found with id: {workout_id}")
        abort(404, message="Workout not found")

    try:
        db.session.delete(workout)
        db.session.commit()

        logger.info(f"Workout deleted successfully with id: {workout_id}")
        return {"message": "Workout deleted successfully"}

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to delete workout: {ex}")
        abort(400, message=f"Failed to delete workout: {ex}")


def get_all_workouts_with_logs(user_id, workout_type=None, start_day=None, end_day=None):
    """
    Get workout logs for a user, optionally filtered by workout_type and date range
    Returns a list of workout logs grouped by workout type
    """
    # Parse date strings to date objects if needed
    if start_day and isinstance(start_day, str):
        start_day = datetime.strptime(start_day, '%Y-%m-%d').date()
    
    if end_day and isinstance(end_day, str):
        end_day = datetime.strptime(end_day, '%Y-%m-%d').date()
    
    # Query workout logs directly
    log_query = WorkoutLogModel.query.filter_by(user_id=user_id)
    
    # Filter by workout_type if provided (convert string to int if needed)
    if workout_type:
        # Map workout type string to integer: 0: cardio, 1: strength, 2: flexibility
        type_map = {
            'cardio': 0,
            'strength': 1,
            'flexibility': 2
        }
        workout_type_int = type_map.get(workout_type.lower(), None)
        if workout_type_int is not None:
            log_query = log_query.filter(WorkoutLogModel.workout_type == workout_type_int)
    
    if start_day:
        log_query = log_query.filter(WorkoutLogModel.log_date >= start_day)
    
    if end_day:
        log_query = log_query.filter(WorkoutLogModel.log_date <= end_day)
    
    workout_logs = log_query.all()
    
    # Group logs by workout_type for response structure
    # Create a simple structure that mimics workouts with logs
    from collections import defaultdict
    
    grouped_logs = defaultdict(list)
    
    for log in workout_logs:
        # Map workout_type int back to string for grouping
        type_map = {0: 'cardio', 1: 'strength', 2: 'flexibility'}
        type_str = type_map.get(log.workout_type, 'cardio')
        grouped_logs[type_str].append(log)
    
    # Create a simple class to hold workout-like structure
    class WorkoutWithLogs:
        def __init__(self, workout_type_str, logs):
            self.id = None
            self.name = workout_type_str.capitalize()
            self.type = workout_type_str
            self.met = None
            self.workout_logs = logs
    
    # Create a list structure compatible with WorkoutWithLogsSchema
    result = []
    for type_str, logs in grouped_logs.items():
        workout_obj = WorkoutWithLogs(type_str, logs)
        result.append(workout_obj)
    
    return result
