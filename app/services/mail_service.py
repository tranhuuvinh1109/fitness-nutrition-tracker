import mailtrap as mt

def send_email(to_email: str, subject: str, html_content: str):
    message = mt.Mail(
        sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
        to=[mt.Address(email=to_email)],
        subject=subject,
        html=html_content,
        category="Integration Test",
    )
    
    try:
        client = mt.MailtrapClient(token="956ec04e6965703cc22781fab783a17e")
        response = client.send(message)
        return {
            "status": "success",
            "message": response
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
