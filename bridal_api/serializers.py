from rest_framework import serializers
from .models import (
    User, Category, Product, Collection, Designer, Appointment,
    Cart, CartItem, Order, OrderItem, Review
)

# -------------------- USER --------------------
class UserSerializer(serializers.ModelSerializer):
    """General purpose User serializer for reading user info"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'date_joined']
        read_only_fields = ['id', 'role', 'date_joined']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data, role=User.CUSTOMER)  # Force role to CUSTOMER
        user.set_password(password)
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

# -------------------- CATEGORY --------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ['id', 'created_at']

# -------------------- PRODUCT --------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'created_at']
        read_only_fields = ['id', 'created_at']

# -------------------- COLLECTION --------------------
class CollectionSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'name', 'description', 'products', 'created_at']
        read_only_fields = ['id', 'created_at']

# -------------------- DESIGNER --------------------
class DesignerSerializer(serializers.ModelSerializer):
    collections = CollectionSerializer(many=True, read_only=True)

    class Meta:
        model = Designer
        fields = ['id', 'name', 'bio', 'collections', 'created_at']
        read_only_fields = ['id', 'created_at']

# -------------------- APPOINTMENT --------------------
class AppointmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    designer = DesignerSerializer(read_only=True)
    designer_id = serializers.PrimaryKeyRelatedField(
        queryset=Designer.objects.all(), write_only=True, source='designer'
    )

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'designer', 'designer_id', 'appointment_date', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

# -------------------- CART ITEM --------------------
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source='product'
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']

# -------------------- CART --------------------
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
        read_only_fields = ['id', 'created_at']

# -------------------- ORDER ITEM --------------------
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source='product'
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']

# -------------------- ORDER --------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'created_at', 'items']
        read_only_fields = ['id', 'user', 'total_price', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total_price = 0

        for item in items_data:
            product = item['product']
            quantity = item['quantity']

            if product.stock < quantity:
                raise serializers.ValidationError(f"Not enough stock for {product.name}")

            product.stock -= quantity
            product.save()

            price = product.price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            total_price += price

        order.total_price = total_price
        order.save()
        return order

# -------------------- REVIEW --------------------
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("user", "created_at")
