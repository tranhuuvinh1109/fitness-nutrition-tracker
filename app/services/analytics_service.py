from datetime import date, timedelta
from sqlalchemy import func
from app.db import db
from app.models.food_log_model import FoodLogModel
from app.models.workout_log_model import WorkoutLogModel
import logging

logger = logging.getLogger(__name__)

def get_nutrition_analytics(user_id, mode=7):
    """
    Get nutrition analytics for the last 'mode' days.
    Returns a list of daily stats (calories, carbs, fat, protein).
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=mode - 1) # Include today, so subtract mode-1

    # Query to sum up nutrients by date
    # We use func.sum and func.date for grouping
    logs = db.session.query(
        FoodLogModel.log_date,
        func.sum(FoodLogModel.calories).label('total_calories'),
        func.sum(FoodLogModel.protein).label('total_protein'),
        func.sum(FoodLogModel.carbs).label('total_carbs'),
        func.sum(FoodLogModel.fat).label('total_fat')
    ).filter(
        FoodLogModel.user_id == user_id,
        FoodLogModel.log_date >= start_date,
        FoodLogModel.log_date <= end_date
    ).group_by(
        FoodLogModel.log_date
    ).all()

    # Convert query results to a dictionary for easy lookup
    data_map = {
        log.log_date: {
            "calories": int(log.total_calories) if log.total_calories else 0,
            "protein": float(log.total_protein) if log.total_protein else 0.0,
            "carbs": float(log.total_carbs) if log.total_carbs else 0.0,
            "fat": float(log.total_fat) if log.total_fat else 0.0
        }
        for log in logs
    }

    # Generate the full list of dates including missing ones
    result = []
    current_date = start_date
    while current_date <= end_date:
        if current_date in data_map:
            stats = data_map[current_date]
            result.append({
                "day": current_date,
                **stats
            })
        else:
            result.append({
                "day": current_date,
                "calories": 0,
                "protein": 0.0,
                "carbs": 0.0,
                "fat": 0.0
            })
        current_date += timedelta(days=1)

    return result


def get_workout_analytics(user_id, mode=7):
    """
    Get workout analytics for the last 'mode' days.
    Returns a list of daily stats (duration_min, calo).
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=mode - 1)

        # Query all logs for the period without grouping
    logs = db.session.query(WorkoutLogModel).filter(
        WorkoutLogModel.user_id == user_id,
        WorkoutLogModel.log_date >= start_date,
        WorkoutLogModel.log_date <= end_date
    ).all()

    # Aggregate by date in Python
    # Map: date -> {duration_min: sum, calo: sum, statuses: set()}
    daily_data = {}
    
    for log in logs:
        if log.log_date not in daily_data:
            daily_data[log.log_date] = {
                "duration_min": 0,
                "calo": 0,
                "statuses": set()
            }
        
        daily_data[log.log_date]["duration_min"] += log.duration_min
        if log.calories_burned:
            daily_data[log.log_date]["calo"] += log.calories_burned
        if log.status is not None:
            daily_data[log.log_date]["statuses"].add(log.status)

    # Generate full list
    result = []
    current_date = start_date
    while current_date <= end_date:
        if current_date in daily_data:
            stats = daily_data[current_date]
            
            # Determine status priority: Completed (1) > Skipped (2) > Planned (0)
            status_set = stats["statuses"]
            final_status = None
            
            if 1 in status_set:
                final_status = 1
            elif 2 in status_set:
                final_status = 2
            else:
                final_status = 0
                
            result.append({
                "day": current_date,
                "duration_min": stats["duration_min"],
                "calo": stats["calo"],
                "status": final_status
            })
        else:
            result.append({
                "day": current_date,
                "duration_min": 0,
                "calo": 0,
                "status": 0
            })
        current_date += timedelta(days=1)

    return result
