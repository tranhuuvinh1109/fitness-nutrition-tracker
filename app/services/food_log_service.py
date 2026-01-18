import logging
from datetime import date

from flask_smorest import abort

from app.db import db
from app.models.food_log_model import FoodLogModel

# Create logger for this module
logger = logging.getLogger(__name__)


def get_all_food_logs(user_id=None, log_date=None, start_day=None, end_day=None):
    """
    Get all food logs, optionally filtered by user_id, log_date, or date range (start_day, end_day)
    """
    from datetime import datetime
    query = FoodLogModel.query

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
            query = query.filter(FoodLogModel.log_date >= start_day)
        
        if end_day:
            if isinstance(end_day, str):
                end_day = datetime.strptime(end_day, '%Y-%m-%d').date()
            query = query.filter(FoodLogModel.log_date <= end_day)

    food_logs = query.all()
    return food_logs


def get_food_log(food_log_id):
    """
    Get food log by id
    """
    food_log = FoodLogModel.query.filter_by(id=food_log_id).first()

    if not food_log:
        logger.error(f"Food log not found with id: {food_log_id}")
        abort(404, message="Food log not found")

    return food_log


def create_food_log(user_id, food_log_data):
    """
    Create a new food log
    """
    try:
        food_log = FoodLogModel(
            user_id=user_id,
            meal_type=food_log_data.get("meal_type"),
            quantity=food_log_data.get("quantity", 1.0),
            log_date=food_log_data["log_date"],
            name=food_log_data["name"],
            calories=food_log_data["calories"],
            protein=food_log_data.get("protein"),
            carbs=food_log_data.get("carbs"),
            fat=food_log_data.get("fat"),
            status=food_log_data.get("status", 1),
        )

        db.session.add(food_log)
        db.session.commit()

        logger.info(f"Food log created successfully with id: {food_log.id}")
        return food_log

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to create food log: {ex}")
        abort(400, message=f"Failed to create food log: {ex}")


def update_food_log(food_log_id, food_log_data):
    """
    Update food log
    """
    food_log = FoodLogModel.query.filter_by(id=food_log_id).first()

    if not food_log:
        logger.error(f"Food log not found with id: {food_log_id}")
        abort(404, message="Food log not found")

    try:
        for key, value in food_log_data.items():
            if value is not None:
                setattr(food_log, key, value)

        db.session.commit()

        logger.info(f"Food log updated successfully with id: {food_log_id}")
        return food_log

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to update food log: {ex}")
        abort(400, message=f"Failed to update food log: {ex}")


def delete_food_log(food_log_id):
    """
    Delete food log
    """
    food_log = FoodLogModel.query.filter_by(id=food_log_id).first()

    if not food_log:
        logger.error(f"Food log not found with id: {food_log_id}")
        abort(404, message="Food log not found")

    try:
        db.session.delete(food_log)
        db.session.commit()

        logger.info(f"Food log deleted successfully with id: {food_log_id}")
        return {"message": "Food log deleted successfully"}

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to delete food log: {ex}")
        abort(400, message=f"Failed to delete food log: {ex}")


def get_food_logs_by_date_range(user_id, start_date, end_date):
    """
    Get food logs for a user within a date range
    """
    food_logs = FoodLogModel.query.filter(
        FoodLogModel.user_id == user_id,
        FoodLogModel.log_date >= start_date,
        FoodLogModel.log_date <= end_date
    ).all()

    return food_logs
