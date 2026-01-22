from marshmallow import Schema, fields, validate

class AnalyticsRequestSchema(Schema):
    mode = fields.Int(validate=validate.OneOf([1, 7, 30]), missing=7, description="Number of days to analyze (1, 7 or 30)")

class AnalyticsItemSchema(Schema):
    day = fields.Date(dump_only=True)
    calories = fields.Int(dump_only=True)
    carbs = fields.Float(dump_only=True)
    fat = fields.Float(dump_only=True)
    protein = fields.Float(dump_only=True)

class AnalyticsResponseSchema(Schema):
    data = fields.List(fields.Nested(AnalyticsItemSchema), dump_only=True)


class AnalyticsWorkoutItemSchema(Schema):
    day = fields.Date(dump_only=True)
    duration_min = fields.Int(dump_only=True)
    calo = fields.Int(dump_only=True)


class AnalyticsWorkoutResponseSchema(Schema):
    data = fields.List(fields.Nested(AnalyticsWorkoutItemSchema), dump_only=True)
