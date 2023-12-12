from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """Регистрация пользователя."""

    class Meta:
        model = User
        fields = ('email', 'username')


class GetTokenSerializer(serializers.Serializer):
    """Получаем username и confirmation code, отдаем токен"""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=32)

    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))
        
        # валидируем код доступа
        if user.confirmation_code != data.get('confirmation_code'):
            raise serializers.ValidationError('Некорректный код подтверждения')
        
        # возвращаем токен для юзера из запроса
        return {'access': str(AccessToken.for_user(user))}
