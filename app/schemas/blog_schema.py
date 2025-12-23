from marshmallow import Schema, fields


class BlogSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    author = fields.Str(required=True)
    image_url = fields.Str()
    summary = fields.Str()

    issued_date = fields.Date()
    effective_date = fields.Date()
    updated_date = fields.Date()
    is_active = fields.Bool()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class BlogCreateSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    author = fields.Str(required=True)
    image_url = fields.Str(required=False)
    summary = fields.Str(required=False)

    issued_date = fields.Date(required=False)
    effective_date = fields.Date(required=False)
    updated_date = fields.Date(required=False)
    is_active = fields.Bool(required=False)


class BlogUpdateSchema(Schema):
    title = fields.Str()
    content = fields.Str()
    author = fields.Str()
    image_url = fields.Str()
    summary = fields.Str()

    issued_date = fields.Date()
    effective_date = fields.Date()
    updated_date = fields.Date()
    is_active = fields.Bool()
