from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        """Проверяем авторизацию пользователя.

        Если метод в запросе является безопасным,
        независимо от наличия авторизации возвращаем True,
        для остальных методов проверяем, что юзер из запроса является админом.
        """
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        """Проверяем, что пользователь является админом"""
        return request.user.is_authenticated and request.user.is_admin


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        """Проверяем авторизацию пользователя.

        Если метод в запросе является безопасным,
        независимо от наличия авторизации возвращаем True,
        для остальных методов проверяем, что юзер из запроса авторизован
        """
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Проверяем права при попытке редактирования или удаления объекта.

        Если метод в запросе является безопасным, то возвращаем True,
        для всех других методов проверяем, что юзер из запроса является
        автором/модератором/админом/суперюзером в случае попытки
        редактирования/удаление сущности, для которой отправлен запрос.
        """
        return (
            request.method in SAFE_METHODS
            or request.user.is_moderator
            or request.user.is_admin
            or obj.author == request.user
        )
