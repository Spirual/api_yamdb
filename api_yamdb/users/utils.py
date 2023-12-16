from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def send_confirmation_code_to_email(email, user):
    """Oтправляет на почту пользователя код подтверждения."""
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
