from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from constants import constants_users as constant
from .managers import UserManager
from .utils import generate_avatar


class Skill(models.Model):
    name = models.CharField(
        verbose_name='Название навыка',
        max_length=constant.MAX_LENGTH_NAME_SKILL
    )

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=constant.MAX_LENGTH_NAME_USER
    )
    surname = models.CharField(
        verbose_name='Фамилия',
        max_length=constant.MAX_LENGTH_SURNAME_USER
    )
    avatar = models.ImageField(
        verbose_name='Аватарка',
        upload_to='avatars/',
        blank=True,
        null=True
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=constant.MAX_LENGTH_PHONE_USER,
        blank=True
    )
    github_url = models.URLField(
        verbose_name='Ссылка на Github',
        blank=True
    )
    about = models.TextField(
        verbose_name='Описание профиля',
        max_length=constant.MAX_LENGTH_ABOUT_USER,
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name='Активный пользователь',
        default=True
    )
    is_staff = models.BooleanField(
        verbose_name='Администратор',
        default=False
    )
    skills = models.ManyToManyField(
        Skill,
        verbose_name='Навыки пользователя',
        related_name='users',
        blank=True
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = generate_avatar(self)
        super().save(*args, **kwargs)
