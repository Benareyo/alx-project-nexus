from django.contrib import admin
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# JWT
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# -------------------- HOME PAGE --------------------
def home(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Welcome to Benareyo Bridal API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #fff0f5;
                color: #333;
                padding: 50px;
            }
            img {
                max-width: 400px;
                height: auto;
                margin: 20px 0;
            }
            h1 {
                font-size: 2.5rem;
                color: #d63384;
            }
            p {
                font-size: 1.2rem;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #d63384;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
            a:hover {
                background-color: #c21870;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to Benareyo Bridal API 🎉</h1>
        <img src="https://images.unsplash.com/photo-1567016540703-c3a93629b1f1?auto=format&fit=crop&w=800&q=80" alt="Bridal Dresses">
        <p>Explore our API documentation and get started with our Bridal E-Commerce backend.</p>
        <a href="/swagger/">Go to API Docs</a>
    </body>
    </html>
    """
    return HttpResponse(html_content)

# -------------------- SWAGGER SCHEMA --------------------
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

# -------------------- URLS --------------------
urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Root home page
    path('', home, name='home'),

    # API
    path('api/', include('bridal_api.urls')),

    # JWT Auth
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
