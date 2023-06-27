from django.contrib import admin
from .models import Products, Bidding, ProductCategory

# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(Products)
admin.site.register(Bidding)
