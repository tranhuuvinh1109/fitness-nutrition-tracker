from flask.views import MethodView
from flask_smorest import Blueprint
from app.services.mail_service import send_email
from app.services.cron_service import send_daily_report
from app.schemas.mail_schema import MailSendSchema

blp = Blueprint("Mail", __name__, description="Mail Service API")

@blp.route("/send", methods=["POST"])
class SendMail(MethodView):
    @blp.arguments(MailSendSchema)
    @blp.response(200)
    def post(self, mail_data):
        """Send an email via SendGrid"""
        result = send_email(
            to_email=mail_data["email"],
            subject=mail_data["subject"],
            html_content=mail_data["content"]
        )
        return result


@blp.route("/send/cron", methods=["POST"])
class SendCronMail(MethodView):
    @blp.response(200)
    def post(self):
        """Trigger daily report email manually"""
        result = send_daily_report()
        if not result:
             return {"message": "Email skipped (CRON_TARGET_EMAIL not set)"}
        return result
