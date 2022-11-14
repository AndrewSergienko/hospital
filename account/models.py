from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.core import validators
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user.set_password(password)
        user.save()

    def create_superuser(self, email, full_name, password=None):
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            is_admin=True
        )
        user.set_password(password)
        user.save()


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True, validators=[validators.EmailValidator()])
    full_name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=100, default='Невідомо')
    is_admin = models.BooleanField(blank=True, default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_all_permissions(self, obj=None):
        return []