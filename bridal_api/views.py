# bridal_api/views.py
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token
from django.shortcuts import get_object_or_404
from django.conf import settings
from PIL import Image
import os

from django.contrib.auth import get_user_model
from .models import (
    Designer, Collection, Dress, VirtualTryOn, FashionShow,
    Appointment, Cart, CartItem, Order
)
from .serializers import (
    UserSerializer, DesignerSerializer, CollectionSerializer,
    DressSerializer, VirtualTryOnSerializer, FashionShowSerializer,
    AppointmentSerializer, CartSerializer, CartItemSerializer, OrderSerializer
)

User = get_user_model()

# -------------------------
# Register view
# -------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # create user + token
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


# -------------------------
# Logout view
# -------------------------
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response({"detail": "Logged out"}, status=status.HTTP_200_OK)


# -------------------------
# ViewSets for core models
# -------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class DesignerViewSet(viewsets.ModelViewSet):
    queryset = Designer.objects.all()
    serializer_class = DesignerSerializer
    permission_classes = [IsAuthenticated]


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]


class DressViewSet(viewsets.ModelViewSet):
    queryset = Dress.objects.all()
    serializer_class = DressSerializer
    permission_classes = [IsAuthenticated]


# -------------------------
# Virtual Try-On
# -------------------------
class VirtualTryOnViewSet(viewsets.ModelViewSet):
    queryset = VirtualTryOn.objects.all()
    serializer_class = VirtualTryOnSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "customer":
            return VirtualTryOn.objects.filter(user=user)
        return super().get_queryset()

    def perform_create(self, serializer):
        # save user then process images
        virtual_tryon = serializer.save(user=self.request.user)

        # Basic overlay process (alpha_composite) - for demo purposes
        try:
            user_image_path = virtual_tryon.user_image.path
            dress_image_path = virtual_tryon.dress.image.path
            result_filename = f"result_{virtual_tryon.id}.png"
            result_dir = os.path.join(settings.MEDIA_ROOT, "virtualtry/results")
            os.makedirs(result_dir, exist_ok=True)
            result_image_path = os.path.join(result_dir, result_filename)

            user_img = Image.open(user_image_path).convert("RGBA")
            dress_img = Image.open(dress_image_path).convert("RGBA")
            dress_img = dress_img.resize(user_img.size)
            combined = Image.alpha_composite(user_img, dress_img)
            combined.save(result_image_path)

            virtual_tryon.result_image.name = f"virtualtry/results/{result_filename}"
            virtual_tryon.save()
        except Exception as e:
            # on error, just keep record without result_image
            # (frontend should handle incomplete results)
            pass


# -------------------------
# FashionShow
# -------------------------
class FashionShowViewSet(viewsets.ModelViewSet):
    queryset = FashionShow.objects.all()
    serializer_class = FashionShowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "designer":
            return FashionShow.objects.filter(designer=user.designer_profile)
        return super().get_queryset()


# -------------------------
# Appointment
# -------------------------
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "customer":
            return Appointment.objects.filter(user=user)
        if user.role == "designer":
            return Appointment.objects.filter(designer=user.designer_profile)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# -------------------------
# Cart & CartItem
# -------------------------
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "customer":
            return Cart.objects.filter(user=user)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "customer":
            return CartItem.objects.filter(cart__user=user)
        return super().get_queryset()


# -------------------------
# Order
# -------------------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "customer":
            return Order.objects.filter(user=user)
        return super().get_queryset()

    def perform_create(self, serializer):
        # If frontend sends cart_id, serializer will attach it (see serializer)
        order = serializer.save(user=self.request.user)
        # order.total_amount will be calculated in model.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
