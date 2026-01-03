import logging

from flask_smorest import abort

from app.db import db
from app.models.food_model import FoodModel

# Create logger for this module
logger = logging.getLogger(__name__)


def get_all_foods():
    """
    Get all foods, optionally filtered by is_vietnamese
    """
    foods = FoodModel.query.all()
    return foods


def get_food(food_id):
    """
    Get food by id
    """
    food = FoodModel.query.filter_by(id=food_id).first()

    if not food:
        logger.error(f"Food not found with id: {food_id}")
        abort(404, message="Food not found")

    return food


def create_food(food_data):
    """
    Create a new food
    """
    try:
        food = FoodModel(
            name=food_data["name"],
            calories=food_data["calories"],
            protein=food_data.get("protein"),
            carbs=food_data.get("carbs"),
            fat=food_data.get("fat"),
            is_vietnamese=food_data.get("is_vietnamese", False)
        )

        db.session.add(food)
        db.session.commit()

        logger.info(f"Food created successfully with id: {food.id}")
        return food

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to create food: {ex}")
        abort(400, message=f"Failed to create food: {ex}")


def update_food(food_id, food_data):
    """
    Update food
    """
    food = FoodModel.query.filter_by(id=food_id).first()

    if not food:
        logger.error(f"Food not found with id: {food_id}")
        abort(404, message="Food not found")

    try:
        if "name" in food_data:
            food.name = food_data["name"]
        if "calories" in food_data:
            food.calories = food_data["calories"]
        if "protein" in food_data:
            food.protein = food_data["protein"]
        if "carbs" in food_data:
            food.carbs = food_data["carbs"]
        if "fat" in food_data:
            food.fat = food_data["fat"]
        if "is_vietnamese" in food_data:
            food.is_vietnamese = food_data["is_vietnamese"]

        db.session.commit()

        logger.info(f"Food updated successfully with id: {food_id}")
        return food

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to update food: {ex}")
        abort(400, message=f"Failed to update food: {ex}")


def delete_food(food_id):
    """
    Delete food
    """
    food = FoodModel.query.filter_by(id=food_id).first()

    if not food:
        logger.error(f"Food not found with id: {food_id}")
        abort(404, message="Food not found")

    try:
        db.session.delete(food)
        db.session.commit()

        logger.info(f"Food deleted successfully with id: {food_id}")
        return {"message": "Food deleted successfully"}

    except Exception as ex:
        db.session.rollback()
        logger.error(f"Failed to delete food: {ex}")
        abort(400, message=f"Failed to delete food: {ex}")
