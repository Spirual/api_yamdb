from rest_framework import routers

from django.urls import include, path

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
)


app_name = 'api'

router_review_v1 = routers.DefaultRouter()
router_review_v1.register('categories', CategoryViewSet)
router_review_v1.register('genres', GenreViewSet)
router_review_v1.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router_review_v1.urls)),
]
