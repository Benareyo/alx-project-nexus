# bridal_api/urls.py
from rest_framework import routers
from django.urls import path, include
from .views import UserViewSet, DesignerViewSet, CollectionViewSet, DressViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'designers', DesignerViewSet, basename='designer')
router.register(r'collections', CollectionViewSet, basename='collection')
router.register(r'dresses', DressViewSet, basename='dress')

urlpatterns = [
    path('', include(router.urls)),
]
