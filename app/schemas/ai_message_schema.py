from marshmallow import Schema, fields, validate


class PlainAIMessageSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(dump_only=True)
    conversation_id = fields.Str(dump_only=True)
    role = fields.Str(validate=validate.OneOf(['user', 'ai']), required=True)
    content = fields.Str(validate=validate.Length(min=1), required=True)
    created_at = fields.DateTime(dump_only=True)


class AIMessageCreateSchema(Schema):
    role = fields.Str(validate=validate.OneOf(['user', 'ai']), required=True)
    content = fields.Str(validate=validate.Length(min=1), required=True)


class AIMessageUpdateSchema(Schema):
    role = fields.Str(validate=validate.OneOf(['user', 'ai']), allow_none=True, required=True)
    content = fields.Str(validate=validate.Length(min=1), allow_none=True, required=True)


class AIMessageResponseSchema(PlainAIMessageSchema):
    pass


class AIMessageAskSchema(Schema):
    message = fields.Str(required=True, validate=validate.Length(min=1))


class ConversationSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    ai_messages = fields.List(fields.Nested(PlainAIMessageSchema), dump_only=True)
