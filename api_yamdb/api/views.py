from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from .mixins import CreateDestiyListModelMixin
from reviews.models import (
    Category,
    Genre,
    Title, Review,
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleWriteSerializer,
    TitleReadSerializer, ReviewSerializer, CommentSerializer,
)
from .permissions import (
    IsAdminOrReadOnly,
    IsAdmin,  # для /users/
    IsAuthenticatedOrReadOnly  # для комментариев, отзывов и /users/me/
)


class CategoryViewSet(CreateDestiyListModelMixin):
    """Вывод категорий произведений."""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateDestiyListModelMixin):
    """Вывод жанров произведений."""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вывод произведений."""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name', 'year', 'category__slug', 'genre__slug'
    )
    http_method_names = (
        'get', 'post', 'patch', 'delete', 'head', 'options',
    )

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(ModelViewSet):
    """Вывод отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)
        title.update_rating()


class CommentViewSet(ModelViewSet):
    """Вывод комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
