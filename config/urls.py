from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    # Esquema en formato OpenAPI (JSON)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Documentación Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),

    # Documentación Redoc (opcional)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


    # URL para la aplicación
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_app.urls')),
    path('api/users/', include('user_app.urls')),
]
