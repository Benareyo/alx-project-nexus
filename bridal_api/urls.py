# bridal_api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .views import (
    UserViewSet, CategoryViewSet, ProductViewSet,
    CollectionViewSet, DesignerViewSet, AppointmentViewSet,
    CartViewSet, CartItemViewSet, OrderViewSet, OrderItemViewSet
)

# -------------------- DRF Router --------------------
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'collections', CollectionViewSet, basename='collections')
router.register(r'designers', DesignerViewSet, basename='designers')
router.register(r'appointments', AppointmentViewSet, basename='appointments')
router.register(r'carts', CartViewSet, basename='carts')
router.register(r'cart-items', CartItemViewSet, basename='cart-items')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order-items', OrderItemViewSet, basename='order-items')

# -------------------- Swagger/OpenAPI --------------------
schema_view = get_schema_view(
    openapi.Info(
        title="Bridal E-Commerce API",
        default_version='v1',
        description="API documentation for Bridal E-Commerce Backend",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[JWTAuthentication],  # for the Authorize button
)

# -------------------- URL Patterns --------------------
urlpatterns = [
    # DRF router urls
    path('', include(router.urls)),

    # JWT Authentication
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger/OpenAPI
    path('swagger<format>\.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
