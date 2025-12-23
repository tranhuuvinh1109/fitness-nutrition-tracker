from marshmallow import Schema, fields, validate


class PlainWaterLogSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(dump_only=True)
    amount_ml = fields.Int(validate=validate.Range(min=1, max=10000), required=True)
    log_date = fields.Date(required=True)
    created_at = fields.DateTime(dump_only=True)


class WaterLogCreateSchema(Schema):
    amount_ml = fields.Int(validate=validate.Range(min=1, max=10000), required=True)
    log_date = fields.Date(required=True)


class WaterLogUpdateSchema(Schema):
    amount_ml = fields.Int(validate=validate.Range(min=1, max=10000), allow_none=True, required=True)
    log_date = fields.Date(allow_none=True, required=True)


class WaterLogResponseSchema(PlainWaterLogSchema):
    pass
