from marshmallow import Schema, fields, validate


class PlainWorkoutSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(validate=validate.Length(min=1, max=255), required=True)
    type = fields.Str(validate=validate.OneOf(['cardio', 'strength', 'flexibility']), required=True)
    met = fields.Float(validate=validate.Range(min=0, max=20), allow_none=True)


class WorkoutCreateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=255), required=True)
    type = fields.Str(validate=validate.OneOf(['cardio', 'strength', 'flexibility']), required=True)
    met = fields.Float(validate=validate.Range(min=0, max=20), allow_none=True)


class WorkoutUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=255), allow_none=True, required=True)
    type = fields.Str(validate=validate.OneOf(['cardio', 'strength', 'flexibility']), allow_none=True, required=True)
    met = fields.Float(validate=validate.Range(min=0, max=20), allow_none=True, required=True)


class WorkoutResponseSchema(PlainWorkoutSchema):
    pass


class WorkoutWithLogsSchema(PlainWorkoutSchema):
    workout_logs = fields.Nested('PlainWorkoutLogSchema', many=True, dump_only=True)
