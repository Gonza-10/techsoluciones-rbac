from django.core.management.base import BaseCommand
from accounts.models import Permission, Role, User


class Command(BaseCommand):
    help = "Crea permisos, roles y usuarios de prueba para el sistema RBAC"

    def handle(self, *args, **options):
        # 1. Crear permisos base
        permisos_base = [
            "LECTURA",
            "EDICIÓN",
            "APROBACIÓN",
            "DECISIÓN",
            "CONTROL",
            "GESTIÓN_TOTAL",
        ]
        perm_objs = {}
        for codigo in permisos_base:
            perm_objs[codigo], _ = Permission.objects.get_or_create(code=codigo)

        # 2. Crear roles y asignar permisos
        roles_def = {
            "Personal": ["LECTURA"],
            "Jefe de Área": ["LECTURA", "EDICIÓN"],
            "Gerente": ["LECTURA", "EDICIÓN", "APROBACIÓN"],
            "Director": ["LECTURA", "EDICIÓN", "APROBACIÓN", "DECISIÓN"],
            "Supervisor": ["LECTURA", "CONTROL"],
            "Administrador del Sistema": ["GESTIÓN_TOTAL"],
        }

        role_objs = {}
        for nombre_rol, permisos in roles_def.items():
            rol, _ = Role.objects.get_or_create(name=nombre_rol)
            rol.permissions.set([perm_objs[p] for p in permisos])
            rol.save()
            role_objs[nombre_rol] = rol

        # 3. Crear usuarios de prueba
        usuarios_demo = [
            ("admin", "123", "Administrador del Sistema"),
            ("carlos_admin", "clave123", "Administrador del Sistema"),
            ("maria_gerente", "clave123", "Gerente"),
            ("juan", "clave123", "Personal"),
            ("ana_personal", "clave123", "Personal"),
        ]

        for username, password, rol_nombre in usuarios_demo:
            user, created = User.objects.get_or_create(username=username)
            user.set_password(password)
            user.role = role_objs[rol_nombre]
            if rol_nombre == "Administrador del Sistema":
                user.is_staff = True
                user.is_superuser = True
            user.save()

        self.stdout.write(self.style.SUCCESS("✅ Permisos, roles y usuarios de prueba creados"))
        self.stdout.write(self.style.SUCCESS("👉 Usuarios de prueba:"))
        for username, password, rol_nombre in usuarios_demo:
            self.stdout.write(f"   - {username} / {password}  ({rol_nombre})")
