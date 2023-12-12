from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .mixins import CreateDestiyListModelMixin
from reviews.models import (
    Category,
    Genre,
    Title,
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleWriteSerializer,
    TitleReadSerializer,
)


class CategoryViewSet(CreateDestiyListModelMixin):
    """Вывод категорий произведений."""

    # permission_classes =
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateDestiyListModelMixin):
    """Вывод жанров произведений."""

    # permission_classes =
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вывод произведений."""

    # permission_classes =
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name', 'year', 'category__slug', 'genre__slug'
    )

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleWriteSerializer
        return TitleReadSerializer
