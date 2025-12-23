from marshmallow import Schema, fields


class ProcedureSchema(Schema):
    id = fields.Int(dump_only=True)
    category = fields.Str(allow_none=True)
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    process_time = fields.Str(allow_none=True)
    authority_level = fields.Str(allow_none=True)
    fee_text = fields.Str(allow_none=True)
    process_steps = fields.Dict(allow_none=True)
    required_documents = fields.Dict(allow_none=True)
    important_notes = fields.Dict(allow_none=True)
    creator = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ProcedureCreateSchema(Schema):
    category = fields.Str(allow_none=True)
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    process_time = fields.Str(allow_none=True)
    authority_level = fields.Str(allow_none=True)
    fee_text = fields.Str(allow_none=True)
    process_steps = fields.Dict(allow_none=True)
    required_documents = fields.Dict(allow_none=True)
    important_notes = fields.Dict(allow_none=True)
    creator = fields.Str(allow_none=True)


class ProcedureUpdateSchema(Schema):
    id = fields.Int(load_only=True) 
    category = fields.Str(allow_none=True)
    title = fields.Str()
    description = fields.Str(allow_none=True)
    process_time = fields.Str(allow_none=True)
    authority_level = fields.Str(allow_none=True)
    fee_text = fields.Str(allow_none=True)
    process_steps = fields.Dict(allow_none=True)
    required_documents = fields.Dict(allow_none=True)
    important_notes = fields.Dict(allow_none=True)
    creator = fields.Str(allow_none=True)
