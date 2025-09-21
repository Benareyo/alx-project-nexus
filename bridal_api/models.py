
from django.db import models
from django.contrib.auth.models import AbstractUser

# ✅ User model (extend Django's built-in user)
class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('designer', 'Designer'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


# ✅ Designer (linked to User if role=designer)
class Designer(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='designer_profile')
    # make name nullable to avoid one-off default migration prompts
    name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else (self.user.username if self.user else "Designer")



# ✅ Collection (group of dresses by designer)
class Collection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name="collections")

    def __str__(self):
        return f"{self.name} ({self.designer.user.username})"


# ✅ Dress
class Dress(models.Model):
    name = models.CharField(max_length=100)
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name="dresses")
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True, related_name="dresses")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=20)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.designer.user.username}"


# ✅ Cart
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.dress.name} x{self.quantity}"


# ✅ Order
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.dress.name} x{self.quantity} (Order {self.order.id})"


# ✅ Payment
class Payment(models.Model):
    METHOD_CHOICES = [
        ('card', 'Card'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash on Delivery'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"


# ✅ Appointment (for trying dresses in person)
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment: {self.user.username} with {self.designer.user.username}"


# ✅ Review (customers leave reviews on dresses)
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.dress.name}"

