from marshmallow import Schema, fields

class ConversationSchema(Schema):
    id = fields.Str()
    user_id = fields.Int()
    title = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class ConversationCreateSchema(Schema):
    title = fields.Str(required=False, allow_none=True)

class ConversationUpdateSchema(Schema):
    title = fields.Str()
    user_id = fields.Int()

class ChatMessageSchema(Schema):
    id = fields.Int()
    conversation_id = fields.Str()
    sender_id = fields.Int(allow_none=True)
    message = fields.Str()
    message_type = fields.Str()
    metadata = fields.Dict(allow_none=True, attribute="message_metadata")  # Map từ message_metadata (model) sang metadata (API)
    created_at = fields.DateTime()
    
class ChatMessageAskSchema(ChatMessageSchema):
    model = fields.String(required=False, allow_none=True)