from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, dni, password=None, **extra_fields):
        if not dni:
            raise ValueError('El DNI es obligatorio')
        user = self.model(dni=dni, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, dni, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(dni, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    dni = models.CharField(max_length=8, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['first_name', 'last_name']
