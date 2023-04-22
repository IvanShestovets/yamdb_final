'''Описание необходимых разрешений проекта.'''
from rest_framework import permissions
from users.models import User


class IsAdminOrReadOnly(permissions.BasePermission):
    '''Позволяет админу и суперюзеру совершать любые действия,
    остальным - только чтение.
    '''

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.role == User.UserRole.ADMIN
            )
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == User.UserRole.ADMIN
        )


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    '''Позволяет автору, админу, модератору и суперюзеру
    совершать любые действия, а остальным - только чтение.
    '''

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == User.UserRole.ADMIN
            or request.user.role == User.UserRole.MODERATOR
        )


class IsAdminOrSuperUser(permissions.BasePermission):
    '''Позволяет админу или суперюзеру совершать любые действия.'''

    edit_methods = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

    def has_permission(self, request, view):
        return bool(
            request.method in self.edit_methods
            and request.user.is_authenticated
            and (
                request.user.role == User.UserRole.ADMIN
                or request.user.is_staff
            )
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in self.edit_methods
            and (
                request.user.role == User.UserRole.ADMIN
                or request.user.is_staff
            )
        )
