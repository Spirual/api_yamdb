from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer
from .utils import send_confirmation_code_to_email

User = get_user_model()


class SignupView(APIView):
    """Регистрация пользователя.

    Если пользователь уже существует, отправляем письмо с кодом подтверждения.
    Если пользователь не существует, валидируем входящие данные,
    сохраняем пользователя в базе и отправляем письмо.
    """
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        email = request.data.get('email')
        if User.objects.filter(username=request.data.get('username'),
                               email=email).exists():
            send_confirmation_code_to_email(email)
            return Response('Код подтверждения отправлен',
                            status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.validated_data.get('email')
        send_confirmation_code_to_email(email)
        return Response(serializer.data, status=status.HTTP_200_OK)
