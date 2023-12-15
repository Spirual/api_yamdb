import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
)

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

    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'year', 'category', 'genre')

    def validate_year(self, value):
        if value > datetime.date.today().year:
            raise serializers.ValidationError(
                'Произведение не может быть из будущего!'
            )
        return value

    def to_representation(self, instance):
        return TitleReadSerializer(instance).data

class TitleReadSerializer(ModelSerializer):
    """Сериализатор вывода произведений."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

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

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10!')
        return value

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        request = self.context['request']
        title = get_object_or_404(Title, id=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                author=request.user, title=title
            ).exists():
                raise serializers.ValidationError(
                    'Можно оставить только один отзыв!'
                )
        return data


class CommentSerializer(ModelSerializer):
    """Вывод списка комментариев."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'review', 'pub_date')
        read_only_fields = ('review',)


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

    role = serializers.CharField(read_only=True)
