from django.contrib import admin
from .models import Product, Signup

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'bulk_price', 'rating','category']
    search_fields = ['name']
    fields = ['name', 'price', 'bulk_price', 'image', 'description', 'features', 'category']


@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'otp')  # Columns shown in the admin table
    search_fields = ('name', 'email', 'phone')        # Enable search box
    list_filter = ('email',) 