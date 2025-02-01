from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором.
    """

    message = "Для этого действия вам необходимо состоять в группе Модераторов."

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderators").exists()


class IsOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsSelf(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем аккаунта.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
