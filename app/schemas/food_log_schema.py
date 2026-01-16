from marshmallow import Schema, fields, validate

from app.models.enums import MealTypeEnum


class PlainFoodLogSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(dump_only=True)
    quantity = fields.Float(validate=validate.Range(min=0.1, max=100), default=1.0)
    log_date = fields.Date(required=True)
    created_at = fields.DateTime(dump_only=True)
    meal_type = fields.Enum(MealTypeEnum, allow_none=True)
    name = fields.Str(required=True)
    calories = fields.Int(required=True)
    protein = fields.Float(allow_none=True)
    carbs = fields.Float(allow_none=True)
    fat = fields.Float(allow_none=True)


class FoodLogCreateSchema(Schema):
    quantity = fields.Float(validate=validate.Range(min=0.1, max=100), default=1.0)
    log_date = fields.Date(required=True)
    meal_type = fields.Enum(MealTypeEnum, allow_none=True)
    name = fields.Str(required=True)
    calories = fields.Int(required=True)
    protein = fields.Float(allow_none=True)
    carbs = fields.Float(allow_none=True)
    fat = fields.Float(allow_none=True)


class FoodLogUpdateSchema(Schema):
    quantity = fields.Float(validate=validate.Range(min=0.1, max=100), allow_none=True)
    log_date = fields.Date(allow_none=True)
    meal_type = fields.Enum(MealTypeEnum, allow_none=True)
    name = fields.Str(allow_none=True)
    calories = fields.Int(allow_none=True)
    protein = fields.Float(allow_none=True)
    carbs = fields.Float(allow_none=True)
    fat = fields.Float(allow_none=True)


class FoodLogResponseSchema(PlainFoodLogSchema):
    pass


class FoodLogWithFoodSchema(PlainFoodLogSchema):
    """Compatibility schema: previously this project included a schema
    that embedded related `Food` details. The `FoodLog` model currently
    stores name/calories directly, so keep this as an alias to the
    plain response schema to preserve router imports.
    """
    pass
