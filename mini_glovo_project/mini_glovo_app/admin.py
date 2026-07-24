from django.contrib import admin
from .models import Category, Store, Product, Review

admin.site.register(Category)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Review)
