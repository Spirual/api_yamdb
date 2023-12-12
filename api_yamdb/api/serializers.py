import datetime

from rest_framework import serializers

from reviews.models import (
    Category,
    Genre,
    Title,
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
