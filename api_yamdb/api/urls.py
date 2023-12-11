from rest_framework import routers

from django.urls import include, path

from .views import (
    CategoryViewSet,
    GenreViewSet,
)

app_name = 'api'

router_review_v1 = routers.DefaultRouter()
router_review_v1.register('categories', CategoryViewSet)
router_review_v1.register('genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(router_review_v1.urls)),
]
