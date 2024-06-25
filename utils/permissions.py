from functools import wraps
from rest_framework.response import Response
from rest_framework.permissions import BasePermission


class AllowedGroupsPermission(BasePermission):
    allowed_groups = ['worker']

    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list('name', flat=True)
        if any(group in self.allowed_groups for group in user_groups):
            return True
        return False


def allowed_groups(allowed_groups):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            groups = request.user.groups.values_list('name', flat=True)
            if any(group in allowed_groups for group in groups):
                return view_func(request, *args, **kwargs)
            return Response({'response': 'You don\'t have permission to perform this action.'}, 403)
        return wrapper_func
    return decorator


def check_allowed(field):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if request.user.role == 'admin':
                return view_func(request, *args, **kwargs)
            else:
                if hasattr(request.user, 'permission_fields'):
                    user_permissions = request.user.permission_fields
                    if getattr(user_permissions, field, False):
                        return view_func(request, *args, **kwargs)
                return Response({'response': 'You don\'t have permission to perform this action.'}, 403)
        return wrapper_func
    return decorator


def allowed_only_admin():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return Response({'response': 'You don\'t have permission to perform this action.'}, 403)
        return wrapper_func
    return decorator
