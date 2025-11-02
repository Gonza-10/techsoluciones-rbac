import datetime
import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from .models import AuditLog

class AuthService:
    @staticmethod
    def autenticar(username: str, password: str):
        # usa el sistema de auth de Django
        return authenticate(username=username, password=password)

    @staticmethod
    def emitir_token(user):
        payload = {
            "sub": user.username,
            "role": user.role.name if user.role else None,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
            "iat": datetime.datetime.utcnow(),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def verificar_token(token: str):
        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return data
        except jwt.PyJWTError:
            return None


class RBACService:
    @staticmethod
    def user_has_permission(user, permission_code: str) -> bool:
        if not user or not user.role:
            return False
        return user.role.has_permission(permission_code)


class AuditService:
    @staticmethod
    def log(user, action: str, extra=None):
        AuditLog.objects.create(user=user, action=action, extra=extra or {})
