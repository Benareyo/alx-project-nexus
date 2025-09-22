# bridal_api/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

# -------------------------
# Custom User
# -------------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("designer", "Designer"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


# -------------------------
# Designer
# -------------------------
class Designer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="designer_profile")
    name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name or self.user.username


# -------------------------
# Collection
# -------------------------
class Collection(models.Model):
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name="collections")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.designer.name or self.designer.user.username})"


# -------------------------
# Dress
# -------------------------
class Dress(models.Model):
    name = models.CharField(max_length=255)
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name="dresses")
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True, related_name="dresses")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="dress_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.designer.user.username}"


# -------------------------
# VirtualTryOn
# -------------------------
class VirtualTryOn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="virtual_tryons")
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE, related_name="virtual_tryons")
    user_image = models.ImageField(upload_to="virtualtry/user_images/")
    result_image = models.ImageField(upload_to="virtualtry/results/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Try-On: {self.user.username} - {self.dress.name}"


# -------------------------
# FashionShow
# -------------------------
class FashionShow(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="fashion_shows")
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name="fashion_shows")
    title = models.CharField(max_length=255)
    scheduled_at = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.collection.name}"


# -------------------------
# Appointment
# -------------------------
class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Appointment: {self.user.username} with {self.designer.user.username} on {self.date}"


# -------------------------
# Cart & CartItem
# -------------------------
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(item.dress.price * item.quantity for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dress.name} x {self.quantity}"


# -------------------------
# Order & OrderItem
# -------------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        if self.cart:
            return sum(item.dress.price * item.quantity for item in self.cart.items.all())
        return self.total_amount

    def save(self, *args, **kwargs):
        # update total_amount from cart items if available
        if self.cart:
            self.total_amount = self.calculate_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
