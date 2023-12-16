from django.contrib.auth.models import AbstractUser
from .validators import validate_username, username_validator
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class CustomUser(AbstractUser):
    """Переопределяем модель User.

    Добавили поля role, bio,
    переопределили поля username и email.
    Остальные поля наследуем от класса AbstractUser как есть,
    так как они удовлетворяют требованиям.
    """

    username = models.CharField(
        verbose_name='Пользователь',
        max_length=150,
        unique=True,
        help_text='Имя пользователя',
        validators=[validate_username, username_validator],
    )
    email = models.EmailField(verbose_name='E-mail', unique=True)
    bio = models.TextField(verbose_name='Биография', blank=True)
    role = models.CharField(
        verbose_name='Роль',
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return (
            self.role == UserRole.ADMIN or self.is_staff or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_user(self):
        return self.role == UserRole.USER

    def __str__(self):
        return self.username
