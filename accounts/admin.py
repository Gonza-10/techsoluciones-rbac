from django.contrib import admin
from .models import User, Role, Permission, AuditLog

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(AuditLog)
