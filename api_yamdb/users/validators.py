from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

username_validator = UnicodeUsernameValidator()


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            'Ошибка: нельзя использовать "me" '
            'в качестве имени пользователя.'
        )
