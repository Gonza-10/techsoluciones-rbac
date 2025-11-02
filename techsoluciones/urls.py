from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # Rutas de nuestra app principal (accounts)
    path('api/', include('accounts.urls')),
]
