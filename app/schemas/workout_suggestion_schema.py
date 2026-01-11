from marshmallow import Schema, fields


class WorkoutSuggestionWorkoutInfoSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
    type = fields.Method("get_type", dump_only=True)
    met = fields.Float(allow_none=True, dump_only=True)
    
    def get_type(self, obj):
        """Convert enum to string"""
        if hasattr(obj.type, 'value'):
            return obj.type.value
        return str(obj.type) if obj.type else None


class WorkoutSuggestionLogInfoSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(dump_only=True)
    workout_id = fields.Str(allow_none=True, dump_only=True)
    duration_min = fields.Int(dump_only=True)
    calories_burned = fields.Int(allow_none=True, dump_only=True)
    log_date = fields.Date(dump_only=True)
    status = fields.Int(dump_only=True)
    note = fields.Str(allow_none=True, dump_only=True)
    workout_type = fields.Int(dump_only=True)
    workout_metadata = fields.Dict(allow_none=True, dump_only=True)
    description = fields.Str(allow_none=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class WorkoutSuggestionItemSchema(Schema):
    log = fields.Nested(WorkoutSuggestionLogInfoSchema, allow_none=True, dump_only=True)
    name = fields.Str(dump_only=True)
    type = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    day_of_week = fields.Int(dump_only=True)


class WorkoutSuggestionResponseSchema(Schema):
    sessions_per_week = fields.Int(dump_only=True)
    start_date = fields.Str(dump_only=True)
    workouts = fields.List(fields.Nested(WorkoutSuggestionItemSchema), dump_only=True)
