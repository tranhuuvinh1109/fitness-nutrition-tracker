import logging

from flask_smorest import abort

from app.db import db
from app.models.goal_model import GoalModel

# Create logger for this module
logger = logging.getLogger(__name__)


def get_all_goals(user_id=None):
    """
    Get all goals, optionally filtered by user_id
    """
    query = GoalModel.query
    if user_id:
        query = query.filter_by(user_id=user_id)

    goals = query.all()
    return goals


def get_goal(goal_id):
    """
    Get goal by id
    """
    goal = GoalModel.query.filter_by(id=goal_id).first()

    if not goal:
        logger.error(f"Goal not found with id: {goal_id}")
        abort(404, message="Goal not found")

    return goal


def create_goal(user_id, goal_data):
    """
    Create a new goal
    """
    try:
        goal = GoalModel(
            user_id=user_id,
            goal_type=goal_data["goal_type"],
            target_weight=goal_data.get("target_weight"),
            daily_calorie_target=goal_data.get("daily_calorie_target")
        )

        db.session.add(goal)
        db.session.commit()

        logger.info(f"Goal created successfully with id: {goal.id}")
        return goal

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to create goal: {ex}")
        abort(400, message=f"Failed to create goal: {ex}")


def update_goal(goal_id, goal_data):
    """
    Update goal
    """
    goal = GoalModel.query.filter_by(id=goal_id).first()

    if not goal:
        logger.error(f"Goal not found with id: {goal_id}")
        abort(404, message="Goal not found")

    try:
        if "goal_type" in goal_data:
            goal.goal_type = goal_data["goal_type"]
        if "target_weight" in goal_data:
            goal.target_weight = goal_data["target_weight"]
        if "daily_calorie_target" in goal_data:
            goal.daily_calorie_target = goal_data["daily_calorie_target"]

        db.session.commit()

        logger.info(f"Goal updated successfully with id: {goal_id}")
        return goal

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to update goal: {ex}")
        abort(400, message=f"Failed to update goal: {ex}")


def delete_goal(goal_id):
    """
    Delete goal
    """
    goal = GoalModel.query.filter_by(id=goal_id).first()

    if not goal:
        logger.error(f"Goal not found with id: {goal_id}")
        abort(404, message="Goal not found")

    try:
        db.session.delete(goal)
        db.session.commit()

        logger.info(f"Goal deleted successfully with id: {goal_id}")
        return {"message": "Goal deleted successfully"}

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to delete goal: {ex}")
        abort(400, message=f"Failed to delete goal: {ex}")
