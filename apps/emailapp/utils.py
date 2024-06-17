from django.core.mail import EmailMessage
import logging

logger = logging.getLogger(__name__)


class Util:
    @staticmethod
    def send_email(data):
        try:
            email = EmailMessage(
                subject=data["email_subject"],
                body=data["email_body"],
                to=[data["to_email"]],
            )
            email.send()
            logger.info(f"Email sent to {data['to_email']}")
        except Exception as e:
            logger.error(
                f"Failed to send email to {data['to_email']}: {str(e)}"
            )
