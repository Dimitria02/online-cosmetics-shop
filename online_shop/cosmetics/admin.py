from django.contrib import admin
from .models import Category, Manufacturer, Product, Client, Order, DetailsOrder

admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(DetailsOrder)
