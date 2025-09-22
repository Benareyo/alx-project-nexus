# bridal_api/admin.py
from django.contrib import admin
from .models import (
    User, Designer, Collection, Dress, VirtualTryOn, FashionShow,
    Appointment, Cart, CartItem, Order
)

admin.site.register(User)
admin.site.register(Designer)
admin.site.register(Collection)
admin.site.register(Dress)
admin.site.register(VirtualTryOn)
admin.site.register(FashionShow)
admin.site.register(Appointment)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
