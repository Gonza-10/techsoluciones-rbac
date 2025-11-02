from rest_framework.response import Response
from rest_framework import status
from .services import AuthService, RBACService
from .models import User

def requiere_permiso(permission_code):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return Response({"error": "Token faltante"}, status=status.HTTP_401_UNAUTHORIZED)

            token = auth.split(" ", 1)[1]
            data = AuthService.verificar_token(token)
            if not data:
                return Response({"error": "Token inválido o expirado"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                user = User.objects.get(username=data["sub"])
            except User.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            if not RBACService.user_has_permission(user, permission_code):
                return Response({"error": "Permiso insuficiente"}, status=status.HTTP_403_FORBIDDEN)

            request.user = user
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
