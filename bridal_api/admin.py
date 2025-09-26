from django.contrib import admin
from .models import User, Category, Product, Collection, Designer, Appointment, Cart, CartItem, Order, OrderItem

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Collection)
admin.site.register(Designer)
admin.site.register(Appointment)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)