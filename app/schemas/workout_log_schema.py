from marshmallow import Schema, fields, validate


class PlainWorkoutLogSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(dump_only=True)
    workout_id = fields.Str(allow_none=True, dump_only=True)
    duration_min = fields.Int(validate=validate.Range(min=1, max=1440), required=True)
    calories_burned = fields.Int(validate=validate.Range(min=0, max=5000), allow_none=True)
    log_date = fields.Date(required=True)
    status = fields.Int(validate=validate.OneOf([0, 1, 2]), allow_none=True)  # 0: planned | 1: completed | 2: skipped
    note = fields.Str(allow_none=True)
    workout_type = fields.Int(validate=validate.OneOf([0, 1, 2]), allow_none=True)  # 0: cardio | 1: strength | 2: flexibility
    workout_metadata = fields.Dict(allow_none=True)
    description = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)


class WorkoutLogCreateSchema(Schema):
    workout_id = fields.Str(allow_none=True)
    duration_min = fields.Int(validate=validate.Range(min=1, max=1440), required=True)
    calories_burned = fields.Int(validate=validate.Range(min=0, max=5000), allow_none=True)
    log_date = fields.Date(required=True)
    status = fields.Int(validate=validate.OneOf([0, 1, 2]), allow_none=True)  # 0: planned | 1: completed | 2: skipped
    note = fields.Str(allow_none=True)
    workout_type = fields.Int(validate=validate.OneOf([0, 1, 2]), allow_none=True)  # 0: cardio | 1: strength | 2: flexibility
    workout_metadata = fields.Dict(allow_none=True)
    description = fields.Str(allow_none=True)


class WorkoutLogUpdateSchema(Schema):
    workout_id = fields.Str(allow_none=True)
    duration_min = fields.Int(validate=validate.Range(min=1, max=1440), allow_none=True)
    calories_burned = fields.Int(validate=validate.Range(min=0, max=5000), allow_none=True)
    log_date = fields.Date(allow_none=True)
    status = fields.Int(validate=validate.OneOf([0, 1, 2]), allow_none=True)  # 0: planned | 1: completed | 2: skipped
    note = fields.Str(allow_none=True)
    workout_type = fields.Int(validate=validate.OneOf([0, 1, 2]), allow_none=True)  # 0: cardio | 1: strength | 2: flexibility
    workout_metadata = fields.Dict(allow_none=True)
    description = fields.Str(allow_none=True)


class WorkoutLogStatusUpdateBodySchema(Schema):
    workout_log_id = fields.Str(required=True)
    status = fields.Int(validate=validate.OneOf([0, 1, 2]), required=True)


class WorkoutLogResponseSchema(PlainWorkoutLogSchema):
    pass
