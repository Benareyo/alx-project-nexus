from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, RegisterView, LoginView, LogoutView, ChangePasswordView,
    CategoryViewSet, ProductViewSet, CollectionViewSet, DesignerViewSet,
    AppointmentViewSet, CartViewSet, CartItemViewSet, OrderViewSet,
    OrderItemViewSet, ReviewListCreateView, InitiatePaymentView, VerifyPaymentView
)

# DRF router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'collections', CollectionViewSet, basename='collection')
router.register(r'designers', DesignerViewSet, basename='designer')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cartitem')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')

urlpatterns = [
    # DRF router URLs
    path('', include(router.urls)),

    # -------------------- AUTH --------------------
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),

    # -------------------- REVIEW --------------------
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),

    # -------------------- PAYMENT --------------------
    path('payments/initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('payments/verify/', VerifyPaymentView.as_view(), name='verify-payment'),
]
