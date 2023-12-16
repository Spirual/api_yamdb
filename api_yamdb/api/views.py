from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
)
from users.utils import send_confirmation_code_to_email
from .filters import TitleFilter
from .mixins import CreateDestiyListModelMixin
from .permissions import IsAdminOrReadOnly, IsAdmin, IsAuthenticatedOrReadOnly
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
from .serializers import SignupSerializer, GetTokenSerializer

User = get_user_model()


APPLY_METHODS = (
    'get',
    'post',
    'patch',
    'delete',
)


class CategoryViewSet(CreateDestiyListModelMixin):
    """Вывод категорий произведений."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateDestiyListModelMixin):
    """Вывод жанров произведений."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """Вывод произведений."""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = APPLY_METHODS

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(ModelViewSet):
    """Вывод отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = APPLY_METHODS

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """Вывод комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = APPLY_METHODS

    def get_review(self):
        return get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id'),
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdmin,)
    http_method_names = APPLY_METHODS
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        serializer = UsersMeSerializer(
            request.user, partial=True, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupView(APIView):
    """Регистрация пользователя.

    Если пользователь уже существует, отправляем письмо с кодом подтверждения.
    Если пользователь не существует, валидируем входящие данные,
    сохраняем пользователя в базе и отправляем письмо.
    """

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        username = serializer.data['username']
        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_username or user_by_email:
            errors = {}
            if user_by_username != user_by_email:
                if user_by_email:
                    errors['email'] = [
                        'Пользователь с таким email уже существует.']
                if user_by_username:
                    errors['username'] = [
                        'Пользователь с таким username уже существует.']
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        user, _ = User.objects.get_or_create(username=username, email=email)
        send_confirmation_code_to_email(user.email, user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    """Получение JWT-токена для в обмен на username и confirmation code."""

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Код подтверждения невалиден'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        token = AccessToken.for_user(user)
        message = {'token': str(token)}
        return Response(message, status=status.HTTP_200_OK)
