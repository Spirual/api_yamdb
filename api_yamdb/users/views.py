from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import SignupSerializer, GetTokenSerializer
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
        existing_user = User.objects.filter(
            username=request.data.get('username')
        ).first()
        if existing_user:
            if existing_user.email != request.data.get('email'):
                serializer.is_valid()
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            send_confirmation_code_to_email(request)
            return Response(request.data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_confirmation_code_to_email(request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(TokenObtainPairView):
    """Получение JWT-токена для в обмен на username и confirmation code."""

    serializer_class = GetTokenSerializer
