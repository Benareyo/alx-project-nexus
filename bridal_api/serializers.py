# bridal_api/serializers.py
from rest_framework import serializers
from .models import User, Designer, Collection, Dress

# Minimal user info for nested display
class UserTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


# Designer Serializer
class DesignerSerializer(serializers.ModelSerializer):
    # Nested read-only user info
    user = UserTinySerializer(read_only=True)
    
    # Accept username to link Designer to User
    user_username = serializers.SlugRelatedField(
        source="user",
        slug_field="username",
        queryset=User.objects.all(),
        write_only=True,
        required=True
    )

    class Meta:
        model = Designer
        fields = ("id", "user", "user_username", "name", "bio", "phone", "email")

    # Validate to prevent duplicates
    def validate(self, attrs):
        user = attrs.get("user")
        if self.instance is None and Designer.objects.filter(user=user).exists():
            raise serializers.ValidationError({
                "user_username": "This user already has a designer profile."
            })
        return attrs

    # Create method
    def create(self, validated_data):
        return Designer.objects.create(**validated_data)


# Collection Serializer
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'


# Dress Serializer
class DressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dress
        fields = '__all__'
