from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# --------------------------------------
# USER MODEL
# --------------------------------------
class User(AbstractUser):
    email = models.EmailField(unique=True)
    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("designer", "Designer"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")

    class Meta:
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["email"]),
            models.Index(fields=["date_joined"]),
        ]

    def __str__(self):
        return self.username

# --------------------------------------
# CATEGORY
# --------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return self.name

# --------------------------------------
# PRODUCT
# --------------------------------------
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

# --------------------------------------
# COLLECTION
# --------------------------------------
class Collection(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    products = models.ManyToManyField(Product, related_name="collections")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

# --------------------------------------
# DESIGNER
# --------------------------------------
class Designer(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    collections = models.ManyToManyField(Collection, related_name="designers")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

# --------------------------------------
# APPOINTMENT
# --------------------------------------
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name="appointments")
    appointment_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Appointment with {self.designer.name} on {self.appointment_date}"

# --------------------------------------
# CART
# --------------------------------------
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Cart ({self.user.username})"

# --------------------------------------
# CART ITEM
# --------------------------------------
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Deleted Product'}"

# --------------------------------------
# ORDER
# --------------------------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

# --------------------------------------
# ORDER ITEM
# --------------------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Deleted Product'}"
