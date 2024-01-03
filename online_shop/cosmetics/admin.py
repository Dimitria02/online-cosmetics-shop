from django.contrib import admin
from .models import Category, Subcategory, Manufacturer, Product, Client, Order, Cart

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Cart)
