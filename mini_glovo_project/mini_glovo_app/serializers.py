from rest_framework import serializers
from .models import (Category, Store, Product, Review)


class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class CategoryNameSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class StoreNameSerializers(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['store_name']


class StoreListSerializers(serializers.ModelSerializer):
    category = CategoryNameSerializers(read_only=True)

    class Meta:
        model = Store
        fields = ['id', 'category', 'store_image', 'store_name']


class StoreEditSerializers(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['category', 'store_name', 'store_image', 'description']


class CategoryDetailSerializers(serializers.ModelSerializer):
    store_category = StoreListSerializers(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'store_category']


class ProductListSerializers(serializers.ModelSerializer):
    store = StoreNameSerializers(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'store', 'product_name', 'price']


class ProductEditSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['store', 'product_name', 'price', 'description', 'product_image']


class ProductDetailSerializers(serializers.ModelSerializer):
    store = StoreNameSerializers(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'store', 'product_image', 'product_name', 'price', 'description']


class ReviewListSerializers(serializers.ModelSerializer):
    store = StoreNameSerializers(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'store', 'user', 'text', 'created_date']


class ReviewEditSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['store', 'text']


class ReviewDetailSerializers(serializers.ModelSerializer):
    store = StoreNameSerializers(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'store', 'user', 'text', 'created_date']


class StoreDetailSerializers(serializers.ModelSerializer):
    category = CategoryNameSerializers(read_only=True)
    product_store = ProductListSerializers(many=True, read_only=True)
    store_reviews = ReviewListSerializers(many=True, read_only=True)

    class Meta:
        model = Store
        fields = ['id', 'category', 'store_name', 'store_image',
                  'store_owner', 'description', 'product_store', 'store_reviews']
        