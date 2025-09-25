# bridal_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # App routes (all bridal_api endpoints will be under /api/)
    path('api/', include('bridal_api.urls')),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login (get tokens)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
