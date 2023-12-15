import secrets

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

User = get_user_model()


def send_confirmation_code_to_email(request):
    # генерируем код подтверждения
    confirmation_code = secrets.token_hex(16)

    # проверяем что пользователь существует в базе
    user = get_object_or_404(
        User,
        username=request.data.get('username'),
    )
    # сохраняем код подтверждения для пользователя из запроса
    user.confirmation_code = confirmation_code
    user.save()

    # отправляем письмо
    send_mail(
        subject='Confirmation code inside',
        message=f'Код подтверждения: {confirmation_code}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.data.get('email')],
    )
