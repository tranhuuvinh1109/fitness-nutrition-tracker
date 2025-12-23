import logging
from datetime import date

from flask_smorest import abort

from app.db import db
from app.models.water_log_model import WaterLogModel

# Create logger for this module
logger = logging.getLogger(__name__)


def get_all_water_logs(user_id=None, log_date=None):
    """
    Get all water logs, optionally filtered by user_id and/or log_date
    """
    query = WaterLogModel.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    if log_date:
        query = query.filter_by(log_date=log_date)

    water_logs = query.all()
    return water_logs


def get_water_log(water_log_id):
    """
    Get water log by id
    """
    water_log = WaterLogModel.query.filter_by(id=water_log_id).first()

    if not water_log:
        logger.error(f"Water log not found with id: {water_log_id}")
        abort(404, message="Water log not found")

    return water_log


def create_water_log(user_id, water_log_data):
    """
    Create a new water log
    """
    try:
        water_log = WaterLogModel(
            user_id=user_id,
            amount_ml=water_log_data["amount_ml"],
            log_date=water_log_data["log_date"]
        )

        db.session.add(water_log)
        db.session.commit()

        logger.info(f"Water log created successfully with id: {water_log.id}")
        return water_log

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to create water log: {ex}")
        abort(400, message=f"Failed to create water log: {ex}")


def update_water_log(water_log_id, water_log_data):
    """
    Update water log
    """
    water_log = WaterLogModel.query.filter_by(id=water_log_id).first()

    if not water_log:
        logger.error(f"Water log not found with id: {water_log_id}")
        abort(404, message="Water log not found")

    try:
        if "amount_ml" in water_log_data:
            water_log.amount_ml = water_log_data["amount_ml"]
        if "log_date" in water_log_data:
            water_log.log_date = water_log_data["log_date"]

        db.session.commit()

        logger.info(f"Water log updated successfully with id: {water_log_id}")
        return water_log

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to update water log: {ex}")
        abort(400, message=f"Failed to update water log: {ex}")


def delete_water_log(water_log_id):
    """
    Delete water log
    """
    water_log = WaterLogModel.query.filter_by(id=water_log_id).first()

    if not water_log:
        logger.error(f"Water log not found with id: {water_log_id}")
        abort(404, message="Water log not found")

    try:
        db.session.delete(water_log)
        db.session.commit()

        logger.info(f"Water log deleted successfully with id: {water_log_id}")
        return {"message": "Water log deleted successfully"}

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to delete water log: {ex}")
        abort(400, message=f"Failed to delete water log: {ex}")


def get_water_logs_by_date_range(user_id, start_date, end_date):
    """
    Get water logs for a user within a date range
    """
    water_logs = WaterLogModel.query.filter(
        WaterLogModel.user_id == user_id,
        WaterLogModel.log_date >= start_date,
        WaterLogModel.log_date <= end_date
    ).all()

    return water_logs


def get_total_water_for_date(user_id, log_date):
    """
    Get total water intake for a specific date
    """
    from sqlalchemy import func
    result = db.session.query(func.sum(WaterLogModel.amount_ml)).filter(
        WaterLogModel.user_id == user_id,
        WaterLogModel.log_date == log_date
    ).scalar()

    return result if result else 0
