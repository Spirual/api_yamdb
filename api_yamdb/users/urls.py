from django.urls import path

from .views import SignupView

app_name = 'users'

urlpatterns = [
    path('v1/auth/signup/',
         SignupView.as_view(),
         name='signup'),
]
