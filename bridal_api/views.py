from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
import requests, os
from rest_framework.views import APIView
from .models import Payment
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    User, Category, Product, Collection, Designer, Appointment,
    Cart, CartItem, Order, OrderItem, Review
)
from .serializers import (
    UserSerializer, UserRegisterSerializer, CategorySerializer,
    ProductSerializer, CollectionSerializer, DesignerSerializer,
    AppointmentSerializer, CartSerializer, CartItemSerializer,
    OrderSerializer, OrderItemSerializer, ReviewSerializer
)
from .pagination import StandardResultsSetPagination
from .permissions import IsAdmin, IsDesigner, IsAdminOrDesigner, IsOwnerOrAdmin

# -------------------- USER --------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["username", "email"]
    ordering_fields = ["date_joined", "username"]
    ordering = ["-date_joined"]

    def get_serializer_class(self):
        if self.action in ["create", "register"]:
            return UserRegisterSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ["create", "register", "login"]:
            return [AllowAny()]
        return [IsAdmin()]

    # ---------------- REGISTER ----------------
    @swagger_auto_schema(
        method='post',
        request_body=UserRegisterSerializer,
        responses={201: UserSerializer}
    )
    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ---------------- LOGIN ----------------
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="User email"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="User password")
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
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
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
    filterset_fields = ["category"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]
    permission_classes = [IsAdminOrDesigner]

# -------------------- COLLECTION --------------------
class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]
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

# -------------------- REVIEW --------------------
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# -------------------- PAYMENT --------------------

class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Payment amount')
            },
            required=['amount']
        ),
        responses={200: openapi.Response('Checkout URL', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'checkout_url': openapi.Schema(type=openapi.TYPE_STRING)}
        ))}
    )

    def post(self, request):
        amount = request.data.get("amount")
        if not amount:
            return Response({"detail": "Amount is required."}, status=400)

        payment = Payment.objects.create(user=request.user, amount=amount)

        headers = {
            "Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "amount": str(amount),
            "currency": "ETB",
            "tx_ref": str(payment.reference),
            "callback_url": "http://localhost:8000/api/payments/verify/",
            "return_url": "http://localhost:8000/payment/success",
            "customization": {
                "title": "Bridal Dress Payment",
                "description": "Payment for bridal dress"
            }
        }

        r = requests.post("https://api.chapa.co/v1/transaction/initialize", json=data, headers=headers)
        res = r.json()

        if res.get("status") == "success":
            return Response({"checkout_url": res["data"]["checkout_url"]})
        else:
            return Response(res, status=400)


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('tx_ref', openapi.IN_QUERY, description="Transaction reference", type=openapi.TYPE_STRING)
        ],
        responses={200: 'Payment verified successfully'}
    )
    
    def get(self, request):
        reference = request.query_params.get("tx_ref")
        if not reference:
            return Response({"detail": "Transaction reference is required."}, status=400)

        headers = {
            "Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}"
        }

        r = requests.get(f"https://api.chapa.co/v1/transaction/verify/{reference}", headers=headers)
        res = r.json()

        if res.get("status") == "success" and res["data"]["status"] == "success":
            try:
                payment = Payment.objects.get(reference=reference)
                payment.status = "successful"
                payment.save()
                return Response({"detail": "Payment verified successfully."})
            except Payment.DoesNotExist:
                return Response({"detail": "Payment not found."}, status=404)
        else:
            return Response({"detail": "Payment verification failed."}, status=400)
