from rest_framework import filters, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import (
    Category,
    Genre,
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    """Вывод категорий произведений."""

    # permission_classes =
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    """Вывод жанров произведений."""

    # permission_classes =
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
