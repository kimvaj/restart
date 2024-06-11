from django.utils.translation import gettext as _
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from common.models.base_models import BaseModel
from django.db import models

from common.models.soft_delete_models import SoftDeleteManager


class UserManager(BaseUserManager, SoftDeleteManager):
    def create_user(
        self,
        email,
        first_name=None,
        last_name=None,
        password=None,
        **extra_fields
    ):
        if not email:
            raise ValueError(_("The Email field must be set"))
        if not first_name:
            raise ValueError(_("The First Name field must be set"))
        if not last_name:
            raise ValueError(_("The Last Name field must be set"))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        first_name=None,
        last_name=None,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(
            email, first_name, last_name, password, **extra_fields
        )


class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # class Meta:
    #     # Explicitly set the database table name
    #     db_table = 'custom_table_name'

    #     # Explicitly set the plural name used in the Django admin
    #     verbose_name = 'profile'
    #     verbose_name_plural = 'profiles'

    # def __str__(self):
    #     return self.email
