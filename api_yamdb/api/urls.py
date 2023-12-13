from rest_framework import routers

from django.urls import include, path

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    UserViewSet,
    UsersMeView,
)
from users.views import SignupView, GetTokenView

app_name = 'api'

router_review_v1 = routers.DefaultRouter()
router_review_v1.register('users', UserViewSet, basename='user',)
router_review_v1.register('categories', CategoryViewSet)
router_review_v1.register('genres', GenreViewSet)
router_review_v1.register('titles', TitleViewSet)
router_review_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review',
)
router_review_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    ReviewViewSet,
    basename='comment',
)

urlpatterns = [
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', GetTokenView.as_view(), name='get_token'),
    path('v1/users/me/', UsersMeView.as_view(), name='users_me'),
    path('v1/', include(router_review_v1.urls))
]
