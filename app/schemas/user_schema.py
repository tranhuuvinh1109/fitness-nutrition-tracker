from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    # Dump only: only read
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    role = fields.Int(required=True)
    balance = fields.Float(dump_only=True)
    time_created = fields.Str(dump_only=True)


class UserUpdateSchema(Schema):
    username = fields.Str(allow_none=True, required=True)
    password = fields.Str(allow_none=True, required=True)
    role = fields.Int(allow_none=True, required=True)


class UserSchema(PlainUserSchema):
    block = fields.Bool(dump_only=True)
    total_used_amount = fields.Float(dump_only=True)
    total_deposited_amount = fields.Float(dump_only=True)


class UserResponseSchema(Schema):
    """Schema for user response without password"""
    id = fields.Str(dump_only=True)
    username = fields.Str(dump_only=True)
    email = fields.Str(dump_only=True)
    role = fields.Int(dump_only=True)
    balance = fields.Float(dump_only=True)
    block = fields.Bool(dump_only=True)
    time_created = fields.Str(dump_only=True)
    total_used_amount = fields.Float(dump_only=True)
    total_deposited_amount = fields.Float(dump_only=True)


class UserExportSchema(Schema):
    role = fields.Int(allow_none=True, required=True)
    search_content = fields.Str(allow_none=True, required=True)


class UserFilterSchema(UserExportSchema):
    page_size = fields.Int(allow_none=True, required=True)
    page = fields.Int(allow_none=True, required=True)


class UserPageSchema(Schema):
    results = fields.List(fields.Nested(UserSchema()))
    total_page = fields.Int()
    total_user = fields.Int()




class UpdateBlockUserSchema(Schema):
    block = fields.Bool(required=True)


class CheckUserExistsSchema(Schema):
    email = fields.Str(required=True)


class UserRegisterSchema(Schema):
    """Schema for user registration - only requires username, email, password"""
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    role = fields.Int()


class UserLoginInputSchema(Schema):
    """Schema for user login - only requires email and password"""
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class UserLoginSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()
    user = fields.Nested(UserResponseSchema)


class UpgradeGuestSchema(Schema):
    """Schema for upgrading guest to user - requires guest credentials and new username"""
    email = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class UpgradeGuestResponseSchema(Schema):
    """Schema for upgrade guest response"""
    message = fields.Str()
    user = fields.Nested(UserResponseSchema)
