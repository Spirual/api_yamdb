from rest_framework import routers

from django.urls import include, path

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
)


app_name = 'api'

router_review_v1 = routers.DefaultRouter()
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
    path('v1/', include(router_review_v1.urls)),
]
