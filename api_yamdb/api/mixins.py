from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class CreateDestiyListModelMixin(mixins.CreateModelMixin,
                                 mixins.ListModelMixin,
                                 mixins.DestroyModelMixin,
                                 GenericViewSet):
    """Миксин только: создаетудаляет объект, возвращает список."""

    pass
