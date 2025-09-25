# bridal_api/permissions.py
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Allow only staff/admin users"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

class IsDesigner(permissions.BasePermission):
    """Allow only users with role == 'designer'"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "role", "") == "designer")

class IsAdminOrDesigner(permissions.BasePermission):
    """
    Read: allow anyone (authenticated).
    Write: allow if user is admin or designer.
    Note: For object-level checks (update/delete), combine with IsOwnerOrReadOnly if needed.
    """
    def has_permission(self, request, view):
        # allow safe methods for authenticated users (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        # write methods require admin or designer role
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or getattr(request.user, "role", "") == "designer"))

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission: allow owner (obj.user) or admin staff to modify.
    Read allowed for authenticated users.
    Assumes target model has a `user` (FK to User) attribute
    """
    def has_permission(self, request, view):
        # require authentication for any access (you could relax GET to allow anonymous if desired)
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # owner or admin
        return (hasattr(obj, "user") and obj.user == request.user) or request.user.is_staff
