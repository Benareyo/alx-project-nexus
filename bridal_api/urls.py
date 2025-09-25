from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
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

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'designers', DesignerViewSet, basename='designer')
router.register(r'collections', CollectionViewSet, basename='collection')
router.register(r'dresses', DressViewSet, basename='dress')
router.register(r'virtualtry', VirtualTryOnViewSet, basename='virtualtry')
router.register(r'fashionshows', FashionShowViewSet, basename='fashionshow')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cartitem')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
