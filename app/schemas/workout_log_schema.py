from marshmallow import Schema, fields, validate


class PlainWorkoutLogSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(dump_only=True)
    workout_id = fields.Str(required=True)
    duration_min = fields.Int(validate=validate.Range(min=1, max=1440), required=True)
    calories_burned = fields.Int(validate=validate.Range(min=0, max=5000), allow_none=True)
    log_date = fields.Date(required=True)
    created_at = fields.DateTime(dump_only=True)


class WorkoutLogCreateSchema(Schema):
    workout_id = fields.Str(required=True)
    duration_min = fields.Int(validate=validate.Range(min=1, max=1440), required=True)
    calories_burned = fields.Int(validate=validate.Range(min=0, max=5000), allow_none=True)
    log_date = fields.Date(required=True)


class WorkoutLogUpdateSchema(Schema):
    workout_id = fields.Str(allow_none=True, required=True)
    duration_min = fields.Int(validate=validate.Range(min=1, max=1440), allow_none=True, required=True)
    calories_burned = fields.Int(validate=validate.Range(min=0, max=5000), allow_none=True, required=True)
    log_date = fields.Date(allow_none=True, required=True)


class WorkoutLogResponseSchema(PlainWorkoutLogSchema):
    pass


class WorkoutLogWithWorkoutSchema(PlainWorkoutLogSchema):
    workout = fields.Nested('PlainWorkoutSchema', dump_only=True)
