# bridal_api/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Designer, Collection, Dress, VirtualTryOn, FashionShow,
    Appointment, Cart, CartItem, Order
)

User = get_user_model()

# -------------------------
# User serializers
# -------------------------
class UserTinySerializer(serializers.ModelSerializer):
    """Minimal info for nested relationships."""
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserSerializer(serializers.ModelSerializer):
    """
    Full user serializer used for registration and admin user management.
    - password is write_only and will be hashed.
    - email is required and unique validation is performed by the model, but we re-check here.
    """
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "password", "role",
            "phone", "address", "first_name", "last_name"
        ]
        read_only_fields = ["id"]

    def validate_email(self, value):
        # Ensure email uniqueness (helps give clearer error messages)
        qs = User.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Support safe password update
        password = validated_data.pop("password", None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# -------------------------
# Designer
# -------------------------
class DesignerSerializer(serializers.ModelSerializer):
    user = UserTinySerializer(read_only=True)
    # allow frontend to set user by id when creating a designer (admin flow)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="user", required=False
    )

    class Meta:
        model = Designer
        fields = ["id", "user", "user_id", "name", "bio", "phone", "email"]
        read_only_fields = ["id", "user"]


# -------------------------
# Collection
# -------------------------
class CollectionSerializer(serializers.ModelSerializer):
    designer = DesignerSerializer(read_only=True)
    designer_id = serializers.PrimaryKeyRelatedField(
        queryset=Designer.objects.all(), source="designer", write_only=True
    )

    class Meta:
        model = Collection
        fields = ["id", "designer", "designer_id", "name", "description", "created_at"]
        read_only_fields = ["id", "created_at"]


# -------------------------
# Dress
# -------------------------
class DressSerializer(serializers.ModelSerializer):
    designer = DesignerSerializer(read_only=True)
    designer_id = serializers.PrimaryKeyRelatedField(
        queryset=Designer.objects.all(), source="designer", write_only=True
    )
    collection = CollectionSerializer(read_only=True)
    collection_id = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(), source="collection", write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Dress
        fields = [
            "id", "name", "designer", "designer_id",
            "collection", "collection_id",
            "price", "description", "size", "stock", "image", "created_at"
        ]
        read_only_fields = ["id", "created_at"]


# -------------------------
# VirtualTryOn
# -------------------------
class VirtualTryOnSerializer(serializers.ModelSerializer):
    user = UserTinySerializer(read_only=True)
    dress = DressSerializer(read_only=True)
    dress_id = serializers.PrimaryKeyRelatedField(
        queryset=Dress.objects.all(), source="dress", write_only=True
    )

    class Meta:
        model = VirtualTryOn
        fields = ["id", "user", "dress", "dress_id", "user_image", "result_image", "created_at"]
        read_only_fields = ["id", "user", "result_image", "created_at"]


# -------------------------
# FashionShow
# -------------------------
class FashionShowSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer(read_only=True)
    collection_id = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(), source="collection", write_only=True
    )
    designer = DesignerSerializer(read_only=True)
    designer_id = serializers.PrimaryKeyRelatedField(
        queryset=Designer.objects.all(), source="designer", write_only=True
    )

    class Meta:
        model = FashionShow
        fields = ["id", "collection", "collection_id", "designer", "designer_id", "title", "scheduled_at", "description"]
        read_only_fields = ["id"]


# -------------------------
# Appointment
# -------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    user = UserTinySerializer(read_only=True)
    designer = DesignerSerializer(read_only=True)
    designer_id = serializers.PrimaryKeyRelatedField(
        queryset=Designer.objects.all(), source="designer", write_only=True
    )

    class Meta:
        model = Appointment
        fields = ["id", "user", "designer", "designer_id", "date", "notes", "status"]
        read_only_fields = ["id", "user"]


# -------------------------
# Cart & CartItem
# -------------------------
class CartItemSerializer(serializers.ModelSerializer):
    dress = DressSerializer(read_only=True)
    dress_id = serializers.PrimaryKeyRelatedField(
        queryset=Dress.objects.all(), source="dress", write_only=True
    )

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
        read_only_fields = ["id", "user", "created_at", "updated_at"]


# -------------------------
# Order
# -------------------------
class OrderSerializer(serializers.ModelSerializer):
    user = UserTinySerializer(read_only=True)
    cart = CartSerializer(read_only=True)
    cart_id = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.all(), source="cart", write_only=True, required=False
    )

    class Meta:
        model = Order
        fields = ["id", "user", "cart", "cart_id", "total_amount", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "total_amount", "created_at", "updated_at"]
