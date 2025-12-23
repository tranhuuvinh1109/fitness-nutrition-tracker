from marshmallow import Schema, fields, validate


class PlainGoalSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(dump_only=True)
    goal_type = fields.Str(validate=validate.OneOf(['lose_weight', 'gain_muscle', 'maintain']), required=True)
    target_weight = fields.Float(validate=validate.Range(min=0, max=500), allow_none=True)
    daily_calorie_target = fields.Int(validate=validate.Range(min=0, max=10000), allow_none=True)
    created_at = fields.DateTime(dump_only=True)


class GoalCreateSchema(Schema):
    goal_type = fields.Str(validate=validate.OneOf(['lose_weight', 'gain_muscle', 'maintain']), required=True)
    target_weight = fields.Float(validate=validate.Range(min=0, max=500), allow_none=True)
    daily_calorie_target = fields.Int(validate=validate.Range(min=0, max=10000), allow_none=True)


class GoalUpdateSchema(Schema):
    goal_type = fields.Str(validate=validate.OneOf(['lose_weight', 'gain_muscle', 'maintain']), allow_none=True, required=True)
    target_weight = fields.Float(validate=validate.Range(min=0, max=500), allow_none=True, required=True)
    daily_calorie_target = fields.Int(validate=validate.Range(min=0, max=10000), allow_none=True, required=True)


class GoalResponseSchema(PlainGoalSchema):
    pass
