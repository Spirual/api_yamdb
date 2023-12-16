import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    if value > datetime.date.today().year:
        raise ValidationError(
            message='Произведение не может быть из будущего!'
        )
