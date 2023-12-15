from django.contrib.auth.models import AbstractUser
from django.db import models

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
        default=UserRole.USER.value[0],
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения', max_length=32, blank=True
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return (
            self.role == UserRole.ADMIN.value[0]
            or self.is_staff
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR.value[0]

    @property
    def is_user(self):
        return self.role == UserRole.USER.value[0]

    def __str__(self):
        return self.username
