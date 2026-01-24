from marshmallow import Schema, fields

class MailSendSchema(Schema):
    email = fields.Email(required=True, description="Recipient email address")
    subject = fields.Str(required=False, missing="Thông báo từ hệ thống", description="Email subject")
    content = fields.Str(required=False, missing="<p>Hello!</p>", description="HTML content of the email")
