# bridal_api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    DesignerViewSet,
    CollectionViewSet,
    DressViewSet,
    VirtualTryOnViewSet,
    FashionShowViewSet,
    AppointmentViewSet,
    CartViewSet,
    CartItemViewSet,
    OrderViewSet,
    RegisterView,
    LogoutView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create DRF router
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'designers', DesignerViewSet)
router.register(r'collections', CollectionViewSet)
router.register(r'dresses', DressViewSet)
router.register(r'virtualtry', VirtualTryOnViewSet)
router.register(r'fashionshows', FashionShowViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'orders', OrderViewSet)

# URL patterns
urlpatterns = [
    path('', include(router.urls)),  # All viewsets
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # JWT refresh
    path('register/', RegisterView.as_view(), name='register'),  # signup
    path('logout/', LogoutView.as_view(), name='logout'),        # logout
]
