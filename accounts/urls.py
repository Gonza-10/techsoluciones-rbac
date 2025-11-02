from django.urls import path
from . import views

urlpatterns = [
    # auth
    path('auth/login/', views.login_view),

    # endpoints protegidos
    path('ver/', views.ver_view),
    path('editar/', views.editar_view),
    path('admin/', views.admin_view),

    # auditoría
    path('auditoria/data/', views.auditoria_api),
    path('auditoria/exportar/', views.auditoria_csv),
    path('auditoria/', views.auditoria_view),

    # interfaz
    path('login/', views.ui_login),
    path('panel/', views.panel_view),
]
