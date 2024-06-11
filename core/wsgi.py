"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
import os

load_dotenv()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")

application = get_wsgi_application()