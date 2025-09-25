# bridal_api/views.py
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import transaction
from PIL import Image
import os

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Designer, Collection, Dress, VirtualTryOn,
    FashionShow, Appointment, Cart, CartItem, Order
)
from .serializers import (
    UserSerializer, DesignerSerializer, CollectionSerializer,
    DressSerializer, VirtualTryOnSerializer, FashionShowSerializer,
    AppointmentSerializer, CartSerializer, CartItemSerializer, OrderSerializer
)
from .permissions import IsOwnerOrAdmin, IsAdminOrDesigner, IsAdmin, IsDesigner

User = get_user_model()

# -------------------------
# Register & Logout (JWT)
# -------------------------
class RegisterView(generics.CreateAPIView):
    """Create account and return JWT tokens"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    """Blacklist a refresh token (logout)"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


# -------------------------
# Users
# -------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


# -------------------------
# Designers
# -------------------------
class DesignerViewSet(viewsets.ModelViewSet):
    """
    - GET: authenticated users can view designers
    - POST: admin can create any Designer; a user with role 'designer' may create own profile which will be linked to their user
    - PATCH/PUT/DELETE: only owner (designer.user) or admin can change
    """
    queryset = Designer.objects.select_related("user").all()
    serializer_class = DesignerSerializer
    permission_classes = [IsAdminOrDesigner, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'email', 'phone']

    def perform_create(self, serializer):
        user = self.request.user
        # Admin can create a designer for any user (expect serializer to accept user_id if you added that)
        if user.is_staff:
            serializer.save()
            return

        # If requester is a designer, auto-attach their user
        if getattr(user, "role", "") == "designer":
            serializer.save(user=user)
            return

        raise PermissionDenied("Only admins or designer users can create designer profiles.")


# -------------------------
# Collections
# -------------------------
class CollectionViewSet(viewsets.ModelViewSet):
    """
    Collections can be created by:
     - admin: create for any designer (if serializer supports designer_id)
     - designer: create collections that will be linked to their Designer profile
    """
    queryset = Collection.objects.select_related("designer__user").all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrDesigner, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'designer__name']

    def perform_create(self, serializer):
        user = self.request.user
        # admin: can set designer explicitly using serializer write field (designer_id)
        if user.is_staff:
            serializer.save()
            return

        if getattr(user, "role", "") == "designer":
            # attach user's designer_profile (ensure it exists through signals or admin)
            if not hasattr(user, "designer_profile"):
                raise PermissionDenied("Designer profile not found for this user.")
            serializer.save(designer=user.designer_profile)
            return

        raise PermissionDenied("Only admin or designers can create collections.")


# -------------------------
# Dresses
# -------------------------
class DressViewSet(viewsets.ModelViewSet):
    """
    Similar rules as Collection:
    - admin can create/update/delete any dress
    - designer users can create dresses attached to their designer_profile
    """
    queryset = Dress.objects.select_related("designer__user", "collection").all()
    serializer_class = DressSerializer
    permission_classes = [IsAdminOrDesigner, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'designer__name', 'collection__name', 'price']

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff:
            serializer.save()
            return

        if getattr(user, "role", "") == "designer":
            if not hasattr(user, "designer_profile"):
                raise PermissionDenied("Designer profile not found for this user.")
            serializer.save(designer=user.designer_profile)
            return

        raise PermissionDenied("Only admin or designer users can create dresses.")


# -------------------------
# Virtual Try-On
# -------------------------
class VirtualTryOnViewSet(viewsets.ModelViewSet):
    queryset = VirtualTryOn.objects.select_related("user", "dress").all()
    serializer_class = VirtualTryOnSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        # Customers see only their own try-ons
        if getattr(user, "role", "") == "customer":
            return VirtualTryOn.objects.filter(user=user)
        return super().get_queryset()

    def perform_create(self, serializer):
        virtual_tryon = serializer.save(user=self.request.user)
        # image overlay: best-effort (non-blocking) — keep small and safe
        try:
            user_img_path = virtual_tryon.user_image.path
            dress_img_path = virtual_tryon.dress.image.path

            result_filename = f"result_{virtual_tryon.id}.png"
            result_dir = os.path.join(settings.MEDIA_ROOT, "virtualtry/results")
            os.makedirs(result_dir, exist_ok=True)
            result_img_path = os.path.join(result_dir, result_filename)

            user_img = Image.open(user_img_path).convert("RGBA")
            dress_img = Image.open(dress_img_path).convert("RGBA")
            dress_img = dress_img.resize(user_img.size)
            combined = Image.alpha_composite(user_img, dress_img)
            combined.save(result_img_path)

            virtual_tryon.result_image.name = f"virtualtry/results/{result_filename}"
            virtual_tryon.save()
        except Exception:
            # don't crash the request if overlay fails
            pass


# -------------------------
# Fashion Shows
# -------------------------
class FashionShowViewSet(viewsets.ModelViewSet):
    queryset = FashionShow.objects.select_related("designer", "collection").all()
    serializer_class = FashionShowSerializer
    permission_classes = [IsAdminOrDesigner, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'designer__name', 'collection__name']

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", "") == "designer":
            # designers only see their own fashion shows
            return FashionShow.objects.filter(designer=user.designer_profile)
        return super().get_queryset()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff:
            serializer.save()
            return
        if getattr(user, "role", "") == "designer":
            serializer.save(designer=user.designer_profile)
            return
        raise PermissionDenied("Only admins or designers can create fashion shows.")


# -------------------------
# Appointments
# -------------------------
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related("user", "designer").all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date', 'status', 'designer__name']

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", "") == "customer":
            return Appointment.objects.filter(user=user)
        if getattr(user, "role", "") == "designer":
            return Appointment.objects.filter(designer=user.designer_profile)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# -------------------------
# Cart & CartItem
# -------------------------
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.select_related("user").prefetch_related("items").all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.select_related("cart", "dress").all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


# -------------------------
# Orders
# -------------------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("user", "cart").all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'created_at']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
