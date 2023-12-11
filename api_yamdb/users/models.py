from django.contrib.auth.models import AbstractUser

from django.db import models

from .validators import username_validator

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'


class CustomUser(AbstractUser):
    """Переопределяем модель User.

    Добавили поля role, bio, переопределили поля username и email.
    Остальные поля наследуем от класса AbstractUser как есть,
    так как они удовлетворяют требованиям.
    """

    ROLE_CHOICES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )

    username = models.CharField(
        verbose_name='Юзернейм',
        max_length=150,
        unique=True,
        help_text=('Поле обязательное. Максимум 150 символов. '
                   'Только буквы, цифры и символы @/./+/-/_ '),
        validators=[username_validator],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
        },
    )
    email = models.EmailField(
        verbose_name='E-mail',
        max_length=254,
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=16,
        choices=ROLE_CHOICES,
        default=USER
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
