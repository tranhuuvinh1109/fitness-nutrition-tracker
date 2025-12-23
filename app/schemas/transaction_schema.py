from marshmallow import Schema, fields


class PlainTransactionSchema(Schema):
    """Base transaction schema"""
    id = fields.Str()
    user_id = fields.Int(required=True)
    status = fields.Int(required=True)  # 0: pending, 1: completed, 2: failed, 3: cancelled
    amount = fields.Float(required=True)
    payment_method = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    additional_data = fields.Dict(allow_none=True)
    code = fields.Str(dump_only=True)  # Last part of UUID v4


class TransactionSchema(PlainTransactionSchema):
    """Full transaction schema with user info"""
    user = fields.Nested("UserResponseSchema", dump_only=True)


class TransactionCreateSchema(Schema):
    """Schema for creating transaction"""
    status = fields.Int(required=True)
    amount = fields.Float(required=True)
    payment_method = fields.Str(required=True)
    additional_data = fields.Dict(allow_none=True)

class TransactionCreateResponseSchema(Schema):
    transaction = fields.Nested(TransactionSchema, required=True)
    qr_image_url = fields.Str(required=True)

class TransactionUpdateSchema(Schema):
    """Schema for updating transaction"""
    status = fields.Int(allow_none=True)
    amount = fields.Float(allow_none=True)
    payment_method = fields.Str(allow_none=True)
    additional_data = fields.Dict(allow_none=True)

class UpdateTransactionStatusSchema(Schema):
    status = fields.Int(required=True)


class TransactionFilterSchema(Schema):
    """Schema for filtering transactions"""
    user_id = fields.Int(allow_none=True)
    status = fields.Int(allow_none=True)
    payment_method = fields.Str(allow_none=True)
    page_size = fields.Int(allow_none=True, default=20)
    page = fields.Int(allow_none=True, default=1)


class TransactionPageSchema(Schema):
    """Schema for paginated transaction results"""
    results = fields.List(fields.Nested(TransactionSchema()))
    total_page = fields.Int()
    total_transactions = fields.Int()


class MBBankWebhookSchema(Schema):
    """Schema for MBBank webhook notification"""
    gateway = fields.Str(required=True)
    transactionDate = fields.Str(required=True)
    accountNumber = fields.Str(required=True)
    subAccount = fields.Str(allow_none=True)
    code = fields.Str(allow_none=True)
    content = fields.Str(required=True)  # Contains transaction ID like "TX66229"
    transferType = fields.Str(required=True)
    description = fields.Str(required=True)
    transferAmount = fields.Float(required=True)
    referenceCode = fields.Str(required=True)
    accumulated = fields.Float(required=True)
    id = fields.Int(required=True)


class WebhookResponseSchema(Schema):
    """Schema for webhook response"""
    success = fields.Bool(required=True)
    message = fields.Str(required=True)
    transaction_id = fields.Str(allow_none=True)
