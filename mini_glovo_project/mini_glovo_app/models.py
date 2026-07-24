from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=64)


class Store(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='store_category')
    store_name = models.CharField(max_length=100)
    description = models.TextField()
    store_image = models.ImageField(null=True, blank=True)
    store_owner = models.IntegerField()


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_store')
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    product_image = models.ImageField(null=True, blank=True)


class Review(models.Model):
    user = models.IntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_reviews')
    text = models.TextField()
    created_date = models.DateField(auto_now_add=True)
