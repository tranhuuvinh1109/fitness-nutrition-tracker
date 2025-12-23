import logging

from flask_smorest import abort

from app.db import db
from app.models.workout_model import WorkoutModel

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
