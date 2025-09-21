# bridal_api/admin.py
from django.contrib import admin
from .models import (
    User,
    Designer,
    Collection,
    Dress,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Payment,
    Appointment,
    Review
)

# Register all models
admin.site.register(User)
admin.site.register(Designer)
admin.site.register(Collection)
admin.site.register(Dress)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Appointment)
admin.site.register(Review)

