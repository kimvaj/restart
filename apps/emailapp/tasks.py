from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email_task(email_data):
    send_mail(
        email_data["subject"],
        email_data["message"],
        settings.DEFAULT_FROM_EMAIL,
        [email_data["recipient"]],
        fail_silently=False,
    )
