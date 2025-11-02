import csv
from datetime import date
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localtime

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .services import AuthService, AuditService
from .decorators import requiere_permiso
from .models import AuditLog

User = get_user_model()


# ==========================
# 🔐 LOGIN Y AUTENTICACIÓN
# ==========================
@csrf_exempt
@api_view(["POST"])
@authentication_classes([])   # sin autenticación previa
@permission_classes([])       # libre acceso al login
def login_view(request):
    username = request.data.get("username", "").strip()
    password = request.data.get("password", "")

    user = AuthService.autenticar(username, password)
    if not user:
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

    token = AuthService.emitir_token(user)
    AuditService.log(user, "login")

    return Response({
        "token": token,
        "user": {
            "username": user.username,
            "role": user.role.name if user.role else None
        }
    })


# ==========================
# 🔓 ENDPOINTS PROTEGIDOS
# ==========================
@api_view(["GET"])
@requiere_permiso("LECTURA")
def ver_view(request):
    AuditService.log(request.user, "ver contenido")
    return Response({"msg": "Contenido visible (permiso: LECTURA)"})


@api_view(["GET"])
@requiere_permiso("EDICIÓN")
def editar_view(request):
    AuditService.log(request.user, "editar contenido")
    return Response({"msg": "Contenido editable (permiso: EDICIÓN)"})


@api_view(["GET"])
@requiere_permiso("GESTIÓN_TOTAL")
def admin_view(request):
    AuditService.log(request.user, "acceso total")
    return Response({"msg": "Acceso completo (permiso: GESTIÓN_TOTAL)"})


# ==========================
# 📊 AUDITORÍA
# ==========================
@api_view(["GET"])
@requiere_permiso("GESTIÓN_TOTAL")
def auditoria_api(request):
    logs = AuditLog.objects.select_related("user").order_by("-timestamp")[:50]
    data = []
    for log in logs:
        data.append({
            "usuario": log.user.username if log.user else "—",
            "accion": log.action,
            "fecha": localtime(log.timestamp).strftime("%d/%m/%Y %H:%M:%S"),
            "extra": log.extra or {},
        })
    return Response({"auditoria": data})


@api_view(["GET"])
@requiere_permiso("GESTIÓN_TOTAL")
def auditoria_csv(request):
    """
    Exporta la auditoría completa a CSV (solo admins),
    con nombre de archivo que incluye la fecha actual.
    """
    logs = AuditLog.objects.select_related("user").order_by("-timestamp")

    hoy = date.today().isoformat()  # ejemplo: 2025-11-02
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="auditoria_techsoluciones_{hoy}.csv"'

    writer = csv.writer(response)
    writer.writerow(["Usuario", "Acción", "Fecha", "Extra"])

    for log in logs:
        writer.writerow([
            log.user.username if log.user else "—",
            log.action,
            log.timestamp.strftime("%d/%m/%Y %H:%M:%S"),
            str(log.extra or "")
        ])

    return response


# ==========================
# 🧭 VISTAS HTML (INTERFAZ)
# ==========================
def ui_login(request):
    """Interfaz del login"""
    return render(request, "login.html")


def panel_view(request):
    """Panel principal"""
    return render(request, "panel.html")


def auditoria_view(request):
    """Vista HTML de la auditoría"""
    return render(request, "auditoria.html")
