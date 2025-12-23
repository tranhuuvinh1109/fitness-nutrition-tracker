from marshmallow import Schema, fields


class AIUsageSchema(Schema):
    """Schema for AI usage records"""
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    conversation_id = fields.Str(dump_only=True)
    model = fields.Str(dump_only=True)
    tokens_used = fields.Int(dump_only=True)
    cost = fields.Float(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    # Include user info
    user = fields.Nested("PlainUserSchema", dump_only=True)


class AIUsagePageSchema(Schema):
    """Schema for paginated AI usage results"""
    results = fields.List(fields.Nested(AIUsageSchema()))
    total_page = fields.Int()
    total_usage = fields.Int()


class AIUsageStatsSchema(Schema):
    """Schema for AI usage statistics"""
    user_id = fields.Int(dump_only=True)
    total_cost = fields.Float(dump_only=True)
    usage_count = fields.Int(dump_only=True)
    current_balance = fields.Float(dump_only=True)
    total_users = fields.Int(dump_only=True)  # For global stats
