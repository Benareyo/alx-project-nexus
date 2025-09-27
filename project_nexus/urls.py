# project_nexus/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# JWT
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger schema
schema_view = get_schema_view(
    openapi.Info(
        title="Bridal E-Commerce API",
        default_version='v1',
        description="API documentation for Bridal E-Commerce Backend",
        contact=openapi.Contact(email="support@bridalapp.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Root view
def root_view(request):
    return JsonResponse({"message": "Welcome to Bridal Backend!"})

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Root
    path('', root_view, name='root'),

    # API
    path('api/', include('bridal_api.urls')),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger / Redoc
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        csrf_exempt(schema_view.without_ui(cache_timeout=0)),
        name='schema-json'
    ),
    path(
        'swagger/',
        csrf_exempt(schema_view.with_ui('swagger', cache_timeout=0)),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        csrf_exempt(schema_view.with_ui('redoc', cache_timeout=0)),
        name='schema-redoc'
    ),
]
