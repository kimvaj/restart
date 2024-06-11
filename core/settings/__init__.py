from __future__ import absolute_import, unicode_literals
from dotenv import load_dotenv
import os


load_dotenv()

__all__ = ("celery_app",)


# Set default DJANGO_ENV to 'dev' if not specified in .env
DJANGO_ENV = os.getenv("DJANGO_ENV", "dev")

if DJANGO_ENV == "prod":
    from .prod import *
else:
    from .dev import *
