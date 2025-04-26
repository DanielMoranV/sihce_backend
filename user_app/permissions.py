from rest_framework.permissions import BasePermission


class IsRole(BasePermission):
    """
    Permite el acceso solo a usuarios con roles específicos.
    Se debe usar con la propiedad `allowed_roles` en la vista.
    """

    def has_permission(self, request, view):
        allowed_roles = getattr(view, 'allowed_roles', [])

        # El usuario debe estar autenticado y tener un rol asignado
        if not request.user or not request.user.is_authenticated:
            return False

        if not hasattr(request.user, 'role') or not request.user.role:
            return False

        return request.user.role.name in allowed_roles
