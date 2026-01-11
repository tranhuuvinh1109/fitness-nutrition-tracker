import logging
from datetime import date, datetime

from flask_smorest import abort

from app.db import db
from app.models.workout_log_model import WorkoutLogModel

# Create logger for this module
logger = logging.getLogger(__name__)


def get_all_workout_logs(user_id=None, log_date=None, start_day=None, end_day=None):
    """
    Get all workout logs, optionally filtered by user_id, log_date, or date range (start_day, end_day)
    """
    query = WorkoutLogModel.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    
    # If log_date is provided, use it (takes precedence over date range)
    if log_date:
        if isinstance(log_date, str):
            log_date = datetime.strptime(log_date, '%Y-%m-%d').date()
        query = query.filter_by(log_date=log_date)
    else:
        # Use date range if provided
        if start_day:
            if isinstance(start_day, str):
                start_day = datetime.strptime(start_day, '%Y-%m-%d').date()
            query = query.filter(WorkoutLogModel.log_date >= start_day)
        
        if end_day:
            if isinstance(end_day, str):
                end_day = datetime.strptime(end_day, '%Y-%m-%d').date()
            query = query.filter(WorkoutLogModel.log_date <= end_day)

    workout_logs = query.all()
    return workout_logs


def get_workout_log(workout_log_id):
    """
    Get workout log by id
    """
    workout_log = WorkoutLogModel.query.filter_by(id=workout_log_id).first()

    if not workout_log:
        logger.error(f"Workout log not found with id: {workout_log_id}")
        abort(404, message="Workout log not found")

    return workout_log


def create_workout_log(user_id, workout_log_data):
    """
    Create a new workout log
    """
    try:
        workout_log = WorkoutLogModel(
            user_id=user_id,
            workout_id=workout_log_data.get("workout_id"),
            duration_min=workout_log_data["duration_min"],
            calories_burned=workout_log_data.get("calories_burned"),
            log_date=workout_log_data["log_date"],
            status=workout_log_data.get("status", 0),
            note=workout_log_data.get("note"),
            workout_type=workout_log_data.get("workout_type", 0),
            workout_metadata=workout_log_data.get("workout_metadata"),
            description=workout_log_data.get("description")
        )

        db.session.add(workout_log)
        db.session.commit()

        logger.info(f"Workout log created successfully with id: {workout_log.id}")
        return workout_log

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to create workout log: {ex}")
        abort(400, message=f"Failed to create workout log: {ex}")


def update_workout_log(workout_log_id, workout_log_data):
    """
    Update workout log
    """
    workout_log = WorkoutLogModel.query.filter_by(id=workout_log_id).first()

    if not workout_log:
        logger.error(f"Workout log not found with id: {workout_log_id}")
        abort(404, message="Workout log not found")

    try:
        if "workout_id" in workout_log_data:
            workout_log.workout_id = workout_log_data["workout_id"]
        if "duration_min" in workout_log_data:
            workout_log.duration_min = workout_log_data["duration_min"]
        if "calories_burned" in workout_log_data:
            workout_log.calories_burned = workout_log_data["calories_burned"]
        if "log_date" in workout_log_data:
            workout_log.log_date = workout_log_data["log_date"]
        if "status" in workout_log_data:
            workout_log.status = workout_log_data["status"]
        if "note" in workout_log_data:
            workout_log.note = workout_log_data["note"]
        if "workout_type" in workout_log_data:
            workout_log.workout_type = workout_log_data["workout_type"]
        if "workout_metadata" in workout_log_data:
            workout_log.workout_metadata = workout_log_data["workout_metadata"]
        if "description" in workout_log_data:
            workout_log.description = workout_log_data["description"]

        db.session.commit()

        logger.info(f"Workout log updated successfully with id: {workout_log_id}")
        return workout_log

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to update workout log: {ex}")
        abort(400, message=f"Failed to update workout log: {ex}")


def delete_workout_log(workout_log_id):
    """
    Delete workout log
    """
    workout_log = WorkoutLogModel.query.filter_by(id=workout_log_id).first()

    if not workout_log:
        logger.error(f"Workout log not found with id: {workout_log_id}")
        abort(404, message="Workout log not found")

    try:
        db.session.delete(workout_log)
        db.session.commit()

        logger.info(f"Workout log deleted successfully with id: {workout_log_id}")
        return {"message": "Workout log deleted successfully"}

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to delete workout log: {ex}")
        abort(400, message=f"Failed to delete workout log: {ex}")


def get_workout_logs_by_date_range(user_id, start_date, end_date):
    """
    Get workout logs for a user within a date range
    """
    workout_logs = WorkoutLogModel.query.filter(
        WorkoutLogModel.user_id == user_id,
        WorkoutLogModel.log_date >= start_date,
        WorkoutLogModel.log_date <= end_date
    ).all()

    return workout_logs
