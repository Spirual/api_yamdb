from django.urls import path

from .views import SignupView, GetTokenView

app_name = 'users'

urlpatterns = [
    # регистрация пользователя
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    # получение токена
    path('v1/auth/token/', GetTokenView.as_view(), name='get_token'),
]
