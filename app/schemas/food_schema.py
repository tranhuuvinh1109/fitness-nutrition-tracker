from marshmallow import Schema, fields, validate


class PlainFoodSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(validate=validate.Length(min=1, max=255), required=True)
    calories = fields.Int(validate=validate.Range(min=0, max=10000), required=True)
    protein = fields.Float(validate=validate.Range(min=0, max=1000), allow_none=True)
    carbs = fields.Float(validate=validate.Range(min=0, max=1000), allow_none=True)
    fat = fields.Float(validate=validate.Range(min=0, max=1000), allow_none=True)
    is_vietnamese = fields.Bool(default=False)


class FoodCreateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=255), required=True)
    calories = fields.Int(validate=validate.Range(min=0, max=10000), required=True)
    protein = fields.Float(validate=validate.Range(min=0, max=1000), allow_none=True)
    carbs = fields.Float(validate=validate.Range(min=0, max=1000), allow_none=True)
    fat = fields.Float(validate=validate.Range(min=0, max=1000), allow_none=True)
    is_vietnamese = fields.Bool(default=False)


class FoodUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=255), allow_none=True, required=True)
    calories = fields.Int(validate=validate.Range(min=0, max=10000), allow_none=True, required=True)
    protein = fields.Float(validate=validate.Range(min=0, max=1000), allow_none=True, required=True)
    carbs = fields.Float(validate=validate.Range(min=0, max=1000), allow_none=True, required=True)
    fat = fields.Float(validate=validate.Range(min=0, max=1000), allow_none=True, required=True)
    is_vietnamese = fields.Bool(allow_none=True, required=True)


class FoodResponseSchema(PlainFoodSchema):
    pass
