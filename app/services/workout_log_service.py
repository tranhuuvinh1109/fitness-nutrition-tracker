import logging
from datetime import date

from flask_smorest import abort

from app.db import db
from app.models.workout_log_model import WorkoutLogModel
from app.models.workout_model import WorkoutModel

# Create logger for this module
logger = logging.getLogger(__name__)


def get_all_workout_logs(user_id=None, log_date=None):
    """
    Get all workout logs, optionally filtered by user_id and/or log_date
    """
    query = WorkoutLogModel.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    if log_date:
        query = query.filter_by(log_date=log_date)

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
    # Validate workout exists
    workout = WorkoutModel.query.filter_by(id=workout_log_data["workout_id"]).first()
    if not workout:
        logger.error(f"Workout not found with id: {workout_log_data['workout_id']}")
        abort(400, message="Workout not found")

    try:
        workout_log = WorkoutLogModel(
            user_id=user_id,
            workout_id=workout_log_data["workout_id"],
            duration_min=workout_log_data["duration_min"],
            calories_burned=workout_log_data.get("calories_burned"),
            log_date=workout_log_data["log_date"]
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

    # Validate workout exists if workout_id is being updated
    if "workout_id" in workout_log_data:
        workout = WorkoutModel.query.filter_by(id=workout_log_data["workout_id"]).first()
        if not workout:
            logger.error(f"Workout not found with id: {workout_log_data['workout_id']}")
            abort(400, message="Workout not found")

    try:
        if "workout_id" in workout_log_data:
            workout_log.workout_id = workout_log_data["workout_id"]
        if "duration_min" in workout_log_data:
            workout_log.duration_min = workout_log_data["duration_min"]
        if "calories_burned" in workout_log_data:
            workout_log.calories_burned = workout_log_data["calories_burned"]
        if "log_date" in workout_log_data:
            workout_log.log_date = workout_log_data["log_date"]

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
