from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.fields import CurrentUserDefault, IntegerField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    EmailField,
    ValidationError,
)

from api_yamdb import settings
from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
)
from users.validators import validate_username, username_validator

User = get_user_model()


class CategorySerializer(ModelSerializer):
    """Вывод списка категорий."""

    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Category


class GenreSerializer(ModelSerializer):
    """Вывод списка жанров."""

    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Genre


class TitleWriteSerializer(ModelSerializer):
    """Сериализатор создания и редактирования произведения."""

    genre = SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'year', 'category', 'genre')

    def to_representation(self, instance):
        return TitleReadSerializer(instance).data


class TitleReadSerializer(ModelSerializer):
    """Сериализатор вывода произведений."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class ReviewSerializer(ModelSerializer):
    """Вывод списка отзывов."""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, id=title_id)
            if Review.objects.filter(
                author=request.user, title=title
            ).exists():
                raise ValidationError('Можно оставить только один отзыв!')
        return data


class CommentSerializer(ModelSerializer):
    """Вывод списка комментариев."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class UserSerializer(ModelSerializer):
    """Вывод данных пользователя"""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UsersMeSerializer(UserSerializer):
    """Вывод данных по запросу PATCH users/me/."""

    role = CharField(read_only=True)


class SignupSerializer(Serializer):
    """Регистрация пользователя."""

    username = CharField(
        max_length=settings.USERNAME_MAX_LENGHT,
        required=True,
        validators=[validate_username, username_validator],
    )
    email = EmailField(
        max_length=settings.EMAIL_MAX_LENGHT,
        required=True,
    )


class GetTokenSerializer(Serializer):
    """Получаем username и confirmation code, отдаем токен"""

    username = CharField(
        max_length=settings.USERNAME_MAX_LENGHT,
        required=True,
        validators=[validate_username, username_validator],
    )
    confirmation_code = CharField()
