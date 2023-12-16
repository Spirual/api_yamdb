from django_filters.rest_framework import (
    FilterSet,
    CharFilter,
)

from reviews.models import Title


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('year', 'name', 'genre__slug', 'category__slug')
