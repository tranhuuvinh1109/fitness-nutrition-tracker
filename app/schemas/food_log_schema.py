from marshmallow import Schema, fields, validate


class PlainFoodLogSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(dump_only=True)
    food_id = fields.Str(required=True)
    quantity = fields.Float(validate=validate.Range(min=0.1, max=100), default=1.0)
    log_date = fields.Date(required=True)
    created_at = fields.DateTime(dump_only=True)


class FoodLogCreateSchema(Schema):
    food_id = fields.Str(required=True)
    quantity = fields.Float(validate=validate.Range(min=0.1, max=100), default=1.0)
    log_date = fields.Date(required=True)


class FoodLogUpdateSchema(Schema):
    food_id = fields.Str(allow_none=True, required=True)
    quantity = fields.Float(validate=validate.Range(min=0.1, max=100), allow_none=True, required=True)
    log_date = fields.Date(allow_none=True, required=True)


class FoodLogResponseSchema(PlainFoodLogSchema):
    pass


class FoodLogWithFoodSchema(PlainFoodLogSchema):
    food = fields.Nested('PlainFoodSchema', dump_only=True)
