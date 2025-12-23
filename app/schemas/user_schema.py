from marshmallow import Schema, fields, validate


class PlainUserSchema(Schema):
    # Dump only: only read
    id = fields.Str(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(validate=validate.Length(min=6, max=255), allow_none=True)
    name = fields.Str(validate=validate.Length(min=1, max=100), allow_none=True)
    created_at = fields.DateTime(dump_only=True)


class UserUpdateSchema(Schema):
    email = fields.Email(allow_none=True, required=True)
    password = fields.Str(validate=validate.Length(min=6, max=255), allow_none=True, required=True)
    name = fields.Str(validate=validate.Length(min=1, max=100), allow_none=True, required=True)



class UserProfileInfoSchema(Schema):
    """Schema for user profile information"""
    age = fields.Int(allow_none=True)
    gender = fields.Str(allow_none=True)
    height_cm = fields.Float(allow_none=True)
    weight_kg = fields.Float(allow_none=True)
    activity_level = fields.Str(allow_none=True)
    updated_at = fields.DateTime(allow_none=True)


class UserResponseSchema(Schema):
    """Schema for user response without password"""
    id = fields.Str(dump_only=True)
    email = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    profile = fields.Nested(UserProfileInfoSchema, allow_none=True)


class CheckUserExistsSchema(Schema):
    email = fields.Str(required=True)


class UserRegisterSchema(Schema):
    """Schema for user registration - only requires email, password, name"""
    email = fields.Email(required=True)
    password = fields.Str(validate=validate.Length(min=6, max=255), required=True)
    name = fields.Str(validate=validate.Length(min=1, max=100), required=True)


class UserLoginInputSchema(Schema):
    """Schema for user login - only requires email and password"""
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UserLoginSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()
    user = fields.Nested(UserResponseSchema)