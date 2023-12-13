from django.contrib.auth.models import AbstractUser

from django.db import models

from .validators import username_validator
from .enums import UserRole


class CustomUser(AbstractUser):
    """Переопределяем модель User.

    Добавили поля role, bio, confirmation_code,
    переопределили поля username и email.
    Остальные поля наследуем от класса AbstractUser как есть,
    так как они удовлетворяют требованиям.
    """

    email = models.EmailField(
        verbose_name='E-mail', max_length=254, unique=True
    )
    bio = models.TextField(verbose_name='Биография', blank=True)
    role = models.CharField(
        verbose_name='Роль',
        max_length=20,
        choices=UserRole.choices(),
        default=UserRole.USER,
    )
    confirmation_code = models.CharField(
        max_length=32,
        blank=True,
        verbose_name='Код подтверждения',
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return (
            self.role == UserRole.ADMIN.value
            or self.is_staff
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR.value

    @property
    def is_user(self):
        return self.role == UserRole.USER.value

    def __str__(self):
        return self.username
