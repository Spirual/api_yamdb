import datetime

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (
    Category,
    Genre,
    Title, Review,
)


class CategorySerializer(serializers.ModelSerializer):
    """Вывод списка категорий."""

    class Meta:
        fields = ('name', 'slug',)
        model = Category

class GenreSerializer(serializers.ModelSerializer):
    """Вывод списка жанров."""

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор создания и редактирования произведения."""

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('name', 'description', 'year', 'category', 'genre')

    def validate_year(self, value):
        if value > datetime.date.today().year:
            raise serializers.ValidationError(
                'Произведение не может быть из будущего!')
        return value


class TitleReadSerializer(serializers.ModelSerializer):
    """ Сериализатор вывода произведений."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating','description', 'genre', 'category')

    def get_rating(self, obj):
        return 100500


class ReviewSerializer(ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Вы уже оставляли отзыв.',
            )
        ]

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10!')
        return value

