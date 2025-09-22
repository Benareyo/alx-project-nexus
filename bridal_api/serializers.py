# bridal_api/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Designer, Collection, Dress, VirtualTryOn, FashionShow,
    Appointment, Cart, CartItem, Order
)

User = get_user_model()

# -------------------------
# User serializers (signup/login)
# -------------------------
class UserTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role", "phone", "address", "first_name", "last_name"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# -------------------------
# Designer
# -------------------------
class DesignerSerializer(serializers.ModelSerializer):
    user = UserTinySerializer(read_only=True)
    user_username = serializers.SlugRelatedField(
        source="user", slug_field="username", queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Designer
        fields = ["id", "user", "user_username", "name", "bio", "phone", "email"]

    def create(self, validated_data):
        user = validated_data.pop("user", None)
        return Designer.objects.create(user=user, **validated_data)


# -------------------------
# Collection
# -------------------------
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "designer", "name", "description", "created_at"]


# -------------------------
# Dress
# -------------------------
class DressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dress
        fields = ["id", "name", "designer", "collection", "price", "description", "size", "stock", "image", "created_at"]


# -------------------------
# Virtual TryOn
# -------------------------
class VirtualTryOnSerializer(serializers.ModelSerializer):
    user = UserTinySerializer(read_only=True)
    dress = DressSerializer(read_only=True)
    dress_id = serializers.PrimaryKeyRelatedField(queryset=Dress.objects.all(), source="dress", write_only=True)

    class Meta:
        model = VirtualTryOn
        fields = ["id", "user", "dress", "dress_id", "user_image", "result_image", "created_at"]
        read_only_fields = ["id", "result_image", "created_at"]


# -------------------------
# FashionShow
# -------------------------
class FashionShowSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer(read_only=True)
    collection_id = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all(), source="collection", write_only=True)
    designer = DesignerSerializer(read_only=True)
    designer_id = serializers.PrimaryKeyRelatedField(queryset=Designer.objects.all(), source="designer", write_only=True)

    class Meta:
        model = FashionShow
        fields = ["id", "collection", "collection_id", "designer", "designer_id", "title", "scheduled_at", "description"]


# -------------------------
# Appointment
# -------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    user = UserTinySerializer(read_only=True)
    designer = DesignerSerializer(read_only=True)
    designer_id = serializers.PrimaryKeyRelatedField(queryset=Designer.objects.all(), source="designer", write_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "user", "designer", "designer_id", "date", "notes", "status"]
        read_only_fields = ["id", "user"]


# -------------------------
# Cart & CartItem
# -------------------------
class CartItemSerializer(serializers.ModelSerializer):
    dress = DressSerializer(read_only=True)
    dress_id = serializers.PrimaryKeyRelatedField(queryset=Dress.objects.all(), source="dress", write_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "cart", "dress", "dress_id", "quantity", "added_at"]
        read_only_fields = ["id", "added_at"]


class CartSerializer(serializers.ModelSerializer):
    user = UserTinySerializer(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "created_at", "updated_at"]


# -------------------------
# Order
# -------------------------
class OrderSerializer(serializers.ModelSerializer):
    user = UserTinySerializer(read_only=True)
    cart = CartSerializer(read_only=True)
    cart_id = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), source="cart", write_only=True, required=False)

    class Meta:
        model = Order
        fields = ["id", "user", "cart", "cart_id", "total_amount", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at", "total_amount"]
