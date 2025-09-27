from rest_framework import viewsets, filters, status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import requests, os

from .models import (
    User, Category, Product, Collection, Designer, Appointment,
    Cart, CartItem, Order, OrderItem, Review, Payment
)
from .serializers import (
    UserSerializer, ChangePasswordSerializer,
    CategorySerializer, ProductSerializer, CollectionSerializer,
    DesignerSerializer, AppointmentSerializer, CartSerializer,
    CartItemSerializer, OrderSerializer, OrderItemSerializer,
    ReviewSerializer
)
from .pagination import StandardResultsSetPagination
from .permissions import IsAdmin, IsDesigner, IsAdminOrDesigner, IsOwnerOrAdmin

# -------------------- HOME PAGE --------------------
def home(request):
    html_content = """
    <html>
        <head>
            <title>Benareyo Bridal API</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; background-color: #fff0f5; margin: 0; padding: 0; }
                .container { padding: 50px; }
                h1 { color: #d63384; font-size: 3em; margin-bottom: 20px; }
                p { font-size: 1.2em; color: #555; }
                img { max-width: 600px; width: 80%; border-radius: 15px; margin-top: 30px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
                a { display: inline-block; margin-top: 20px; font-size: 1.2em; text-decoration: none; color: white; background-color: #d63384; padding: 10px 20px; border-radius: 8px; }
                a:hover { background-color: #c02677; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to Benareyo Bridal 🎉</h1>
                <p>Your ultimate API for bridal collections, designers, and appointments.</p>
                <img src="https://images.unsplash.com/photo-1600180758895-9b8a9f78827b?auto=format&fit=crop&w=800&q=80" alt="Bridal">
                <br>
                <a href="/swagger/">Explore API Docs</a>
            </div>
        </body>
    </html>
    """
    return HttpResponse(html_content)


# -------------------- USER CRUD (Admin only) --------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["username", "email"]
    ordering_fields = ["date_joined", "username"]
    ordering = ["-date_joined"]
    permission_classes = [IsAdmin]


# -------- REGISTER --------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["username", "email", "password"]
        )
    )
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response({"detail": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"detail": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)


# -------- LOGIN --------
class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['email', 'password']
        )
    )
    def post(self, request):
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
            "access": str(refresh.access_token),
            "role": user.role
        })


# -------- LOGOUT --------
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"status": "Logged out successfully"}, status=status.HTTP_200_OK)


# -------- CHANGE PASSWORD --------
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")
            if not user.check_password(old_password):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({"status": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        request_body=DesignerSerializer,
        responses={201: DesignerSerializer}
    )
    def create(self, request, *args, **kwargs):
        if not request.user.role == "admin":
            raise PermissionDenied("Only admins can register designers.")
        return super().create(request, *args, **kwargs)


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
    filterset_fields = ["user", "status", "items__product__category"]
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
            properties={'amount': openapi.Schema(type=openapi.TYPE_NUMBER)},
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
        headers = {"Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}", "Content-Type": "application/json"}
        data = {
            "amount": str(amount),
            "currency": "ETB",
            "tx_ref": str(payment.reference),
            "callback_url": "http://localhost:8000/api/payments/verify/",
            "return_url": "http://localhost:8000/payment/success",
            "customization": {"title": "Bridal Dress Payment", "description": "Payment for bridal dress"}
        }
        r = requests.post("https://api.chapa.co/v1/transaction/initialize", json=data, headers=headers)
        res = r.json()
        if res.get("status") == "success":
            return Response({"checkout_url": res["data"]["checkout_url"]})
        return Response(res, status=400)


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('tx_ref', openapi.IN_QUERY, description="Transaction reference", type=openapi.TYPE_STRING)],
        responses={200: 'Payment verified successfully'}
    )
    def get(self, request):
        reference = request.query_params.get("tx_ref")
        if not reference:
            return Response({"detail": "Transaction reference is required."}, status=400)
        headers = {"Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}"}
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
        return Response({"detail": "Payment verification failed."}, status=400)
