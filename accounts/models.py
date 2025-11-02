from django.db import models
from django.contrib.auth.models import AbstractUser

# Permiso: lo que antes era un string en una lista
class Permission(models.Model):
    code = models.CharField(max_length=100, unique=True)  # ej: LECTURA
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.code

# Rol: tiene muchos permisos
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)  # ej: Gerente
    permissions = models.ManyToManyField(Permission, blank=True)

    def has_permission(self, code: str) -> bool:
        code = code.upper()
        # igual que en tu Flask: si tiene GESTIÓN_TOTAL, puede todo
        return (
            self.permissions.filter(code=code).exists()
            or self.permissions.filter(code="GESTIÓN_TOTAL").exists()
        )

    def __str__(self):
        return self.name

# Usuario: es el usuario de Django pero con un campo "role"
class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

# Auditoría: para registrar acciones
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    extra = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action}"
