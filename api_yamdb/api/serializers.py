from rest_framework import serializers

from reviews.models import (
    Category,
    Genre,
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
