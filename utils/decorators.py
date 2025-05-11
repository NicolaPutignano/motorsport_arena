from functools import wraps
from rest_framework.exceptions import PermissionDenied

ROLES_HIERARCHY = {
    "MEMBER": 1,
    "CREATOR": 2,
    "SUPERVISOR": 3,
    "MANAGER": 4,
    "ADMIN": 5,
}


def require_role(*required_roles):
    def decorator(view_method):
        @wraps(view_method)
        def _wrapped_view(self, request, *args, **kwargs):
            user = request.user
            if not user or not user.is_authenticated:
                raise PermissionDenied("Autenticazione richiesta.")

            user_role = getattr(user, 'role', None)
            if user_role not in ROLES_HIERARCHY:
                raise PermissionDenied("Ruolo non definito correttamente.")

            user_level = ROLES_HIERARCHY[user_role]
            for role in required_roles:
                if role in ROLES_HIERARCHY and user_level >= ROLES_HIERARCHY[role]:
                    return view_method(self, request, *args, **kwargs)

            raise PermissionDenied(f"Permesso negato. Richiede uno dei ruoli: {required_roles}")

        return _wrapped_view

    return decorator
