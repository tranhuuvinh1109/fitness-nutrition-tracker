from marshmallow import Schema, fields

from app.models.enums import MealTypeEnum
from app.schemas.food_log_schema import PlainFoodLogSchema


class FoodSuggestionRequestSchema(Schema):
    dayPlan = fields.Str(allow_none=True)
    meal_type = fields.Enum(MealTypeEnum, allow_none=True)


class FoodSuggestionItemSchema(Schema):
    log = fields.Nested(PlainFoodLogSchema, allow_none=True, dump_only=True)
    name = fields.Str(dump_only=True)
    meal_type = fields.Str(dump_only=True)
    calories = fields.Int(dump_only=True)
    day_of_week = fields.Int(dump_only=True)
    description = fields.Str(dump_only=True)


class FoodSuggestionResponseSchema(Schema):
    date = fields.Str(dump_only=True)
    foods = fields.List(fields.Nested(FoodSuggestionItemSchema), dump_only=True)
