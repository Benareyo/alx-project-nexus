# bridal_api/views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    User, Category, Product, Collection, Designer, Appointment,
    Cart, CartItem, Order, OrderItem
)
from .serializers import (
    UserSerializer, UserRegisterSerializer, CategorySerializer,
    ProductSerializer, CollectionSerializer, DesignerSerializer,
    AppointmentSerializer, CartSerializer, CartItemSerializer,
    OrderSerializer, OrderItemSerializer
)
from .pagination import StandardResultsSetPagination
from .permissions import IsAdmin, IsDesigner, IsAdminOrDesigner, IsOwnerOrAdmin


# -------------------- USER --------------------
class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD API for users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["username", "email"]
    ordering_fields = ["date_joined", "username"]
    ordering = ["-date_joined"]
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        method='post',
        request_body=UserRegisterSerializer,
        responses={201: UserSerializer}
    )
    @action(detail=False, methods=["post"], url_path="register", permission_classes=[])
    def register(self, request):
        """
        Register a new user (customer, designer, or admin). No authentication required.
        """
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password')
            },
            required=['email', 'password']
        ),
        responses={200: openapi.Response('JWT Token', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                'access': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ))}
    )
    @action(detail=False, methods=['post'], url_path='login', permission_classes=[])
    def login(self, request):
        """
        Obtain JWT token pair for a user.
        """
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response({"detail": "Email and password required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.check_password(password):
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })


# -------------------- CATEGORY --------------------
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]
    permission_classes = [IsAdminOrDesigner]


# -------------------- PRODUCT --------------------
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "designer", "collection"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]
    permission_classes = [IsAdminOrDesigner]


# -------------------- DESIGNER --------------------
class DesignerViewSet(viewsets.ModelViewSet):
    queryset = Designer.objects.all()
    serializer_class = DesignerSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "bio"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]
    permission_classes = [IsAdmin]


# -------------------- COLLECTION --------------------
class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at"]
    ordering = ["title"]
    permission_classes = [IsAdminOrDesigner]


# -------------------- APPOINTMENT --------------------
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["notes"]
    ordering_fields = ["appointment_date", "created_at"]
    ordering = ["-appointment_date"]
    permission_classes = [IsOwnerOrAdmin]


# -------------------- CART --------------------
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsOwnerOrAdmin]


# -------------------- CART ITEM --------------------
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["cart", "product"]
    permission_classes = [IsOwnerOrAdmin]


# -------------------- ORDER --------------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["user", "status"]
    ordering_fields = ["created_at", "total_price"]
    ordering = ["-created_at"]
    permission_classes = [IsOwnerOrAdmin]


# -------------------- ORDER ITEM --------------------
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["order", "product"]
    permission_classes = [IsOwnerOrAdmin]
