from marshmallow import Schema, fields


class WorkoutSuggestionWorkoutInfoSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    type = fields.Str()
    met = fields.Float(allow_none=True)


class WorkoutSuggestionLogInfoSchema(Schema):
    id = fields.Str()
    user_id = fields.Str()
    workout_id = fields.Str()
    duration_min = fields.Int()
    calories_burned = fields.Int(allow_none=True)
    log_date = fields.Date()
    created_at = fields.DateTime()


class WorkoutSuggestionItemSchema(Schema):
    workout = fields.Nested(WorkoutSuggestionWorkoutInfoSchema)
    log = fields.Nested(WorkoutSuggestionLogInfoSchema, allow_none=True)
    description = fields.Str()
    day_of_week = fields.Int()


class WorkoutSuggestionResponseSchema(Schema):
    sessions_per_week = fields.Int()
    start_date = fields.Str()
    workouts = fields.List(fields.Nested(WorkoutSuggestionItemSchema))
