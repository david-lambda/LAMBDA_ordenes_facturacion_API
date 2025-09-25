from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def require_permission(perm_codename:list, app_label:str=None):
    """
    Decorador que valida si el usuario autenticado tiene el permiso indicado.
    
    Args:
        perm_codename (str): codename del permiso, ej: 'can_add_user'
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view, request, *args, **kwargs):
            #Validar si el usuario está autenticado
            if not request.user.is_authenticated:
                return Response(
                    {"error": "No autenticado."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            #Agrega el app_label a los permisos
            full_perms = [f"{app_label}.{p}" for p in perm_codename]

            #Valida si el usuario tiene los permisos
            if not request.user.has_perms(full_perms):
                return Response({"error": "No autorizado."}, status=status.HTTP_401_UNAUTHORIZED)
            return view_func(view, request, *args, **kwargs)
        return _wrapped_view
    return decorator