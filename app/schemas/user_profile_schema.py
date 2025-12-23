from marshmallow import Schema, fields, validate


class PlainUserProfileSchema(Schema):
    user_id = fields.Str(dump_only=True)
    age = fields.Int(validate=validate.Range(min=0, max=150), allow_none=True)
    gender = fields.Str(validate=validate.OneOf(['male', 'female', 'other']), allow_none=True)
    height_cm = fields.Float(validate=validate.Range(min=0, max=300), allow_none=True)
    weight_kg = fields.Float(validate=validate.Range(min=0, max=500), allow_none=True)
    activity_level = fields.Str(validate=validate.OneOf(['low', 'medium', 'high']), allow_none=True)
    updated_at = fields.DateTime(dump_only=True)


class UserProfileUpdateSchema(Schema):
    age = fields.Int(validate=validate.Range(min=0, max=150), allow_none=True, required=True)
    gender = fields.Str(validate=validate.OneOf(['male', 'female', 'other']), allow_none=True, required=True)
    height_cm = fields.Float(validate=validate.Range(min=0, max=300), allow_none=True, required=True)
    weight_kg = fields.Float(validate=validate.Range(min=0, max=500), allow_none=True, required=True)
    activity_level = fields.Str(validate=validate.OneOf(['low', 'medium', 'high']), allow_none=True, required=True)


class UserProfileResponseSchema(PlainUserProfileSchema):
    pass
