# bridal_api/serializers.py
from rest_framework import serializers
from .models import (
    User, Category, Product, Collection, Designer, Appointment,
    Cart, CartItem, Order, OrderItem
)

# -------------------- USER --------------------
class UserSerializer(serializers.ModelSerializer):
    """For returning user info including role."""
    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]

class UserRegisterSerializer(serializers.ModelSerializer):
    """For registering a new user with role validation."""
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
    
    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]

    def validate_role(self, value):
        valid_roles = [choice[0] for choice in User.ROLE_CHOICES]  # Ensure matches model choices
        if value not in valid_roles:
            raise serializers.ValidationError(f'"{value}" is not a valid role. Choose from {valid_roles}.')
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  # hash the password
        user.save()
        return user

# -------------------- CATEGORY --------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

# -------------------- PRODUCT --------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

# -------------------- COLLECTION --------------------
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"

# -------------------- DESIGNER --------------------
class DesignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designer
        fields = "__all__"

# -------------------- APPOINTMENT --------------------
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

# -------------------- CART ITEM --------------------
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]

# -------------------- CART --------------------
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "created_at", "items"]

# -------------------- ORDER ITEM --------------------
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]

# -------------------- ORDER --------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "total_price", "status", "created_at", "items"]
