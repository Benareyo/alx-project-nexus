# bridal_api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet, CategoryViewSet, ProductViewSet,
    CollectionViewSet, DesignerViewSet, AppointmentViewSet,
    CartViewSet, CartItemViewSet, OrderViewSet, OrderItemViewSet,
    ReviewListCreateView, InitiatePaymentView, VerifyPaymentView
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

# -------------------- URL Patterns --------------------
urlpatterns = [
    # DRF ViewSets
    path('', include(router.urls)),

    # Reviews (APIView)
    path("reviews/", ReviewListCreateView.as_view(), name="reviews"),

    # Payment endpoints
    path("payments/initiate/", InitiatePaymentView.as_view(), name="initiate-payment"),
    path("payments/verify/", VerifyPaymentView.as_view(), name="verify-payment"),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
