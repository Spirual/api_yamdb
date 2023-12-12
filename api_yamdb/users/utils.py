from django.core.mail import send_mail
from django.conf import settings
import secrets


def send_confirmation_code_to_email(email):
    # генерируем код подтверждения
    confirmation_code = secrets.token_hex(16)

    # отправляем письмо
    send_mail(
        subject='Confirmation code inside',
        message=f'Код подтверждения: {confirmation_code}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
