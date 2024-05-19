from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from .managers import Manager
from uuid import uuid4

class User(AbstractBaseUser):
    uuid = models.UUIDField(
        verbose_name="UUID",
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid4
    )
    username = models.CharField(
        verbose_name="Логин",
        unique=True,
        max_length=32,
    )
    email = models.CharField(
        verbose_name="Эл. почта",
        unique=True,
        max_length=64,
    )
    password = models.CharField(
        verbose_name="Пароль",
        max_length=128,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=32,
        blank=True,
    )
    middle_name = models.CharField(
        verbose_name="Отчество",
        max_length=32,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=32,
        blank=True,
    )
    
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    
    @property
    def is_staff(self):
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    objects = Manager()

    def __str__(self):
        return self.username    
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'