from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

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
    TitleReadSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    UsersMeSerializer,
)
from .permissions import (
    IsAdminOrReadOnly,
    IsAdmin,
    IsAuthenticatedOrReadOnly
)
from .filters import TitleFilter

User = get_user_model()


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


class TitleViewSet(ModelViewSet):
    """Вывод произведений."""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
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
    http_method_names = (
        'get', 'post', 'patch', 'delete', 'head', 'options',
    )

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
    http_method_names = (
        'get', 'post', 'patch', 'delete', 'head', 'options',
    )

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdmin,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'


class UsersMeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Возвращает текущего пользователя."""
        return get_object_or_404(User, username=self.request.user.username)

    def get_serializer_class(self):
        """Возвращает сериализатор для объекта в зависимости от метода."""
        if self.request.method == 'PATCH':
            return UsersMeSerializer
        return UserSerializer

    def get(self, request):
        """Метод GET."""
        me = self.get_object()
        serializer = self.get_serializer_class()(me)
        return Response(serializer.data)

    def patch(self, request):
        """Метод PATCH."""
        me = self.get_object()
        serializer = self.get_serializer_class()(me,
                                                 data=request.data,
                                                 partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
