from django.urls import path
from .views import (CategoryListAPIView, CategoryDetailAPIView,
                    StoreListAPIView, StoreDetailAPIView,
                    StoreCreateAPIView, StoreUpdateAPIView, StoreDeleteAPIView,
                    ProductListAPIView, ProductDetailAPIView,
                    ProductCreateAPIView, ProductUpdateAPIView, ProductDeleteAPIView,
                    ReviewListAPIView, ReviewDetailAPIView,
                    ReviewCreateAPIView, ReviewUpdateAPIView, ReviewDeleteAPIView)

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),

    path('stores/', StoreListAPIView.as_view(), name='store_list'),
    path('stores/<int:pk>/', StoreDetailAPIView.as_view(), name='store_detail'),
    path('store_create/', StoreCreateAPIView.as_view(), name='store_create'),
    path('store_update/<int:pk>/', StoreUpdateAPIView.as_view(), name='store_update'),
    path('store_delete/<int:pk>/', StoreDeleteAPIView.as_view(), name='store_delete'),

    path('products/', ProductListAPIView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('product_create/', ProductCreateAPIView.as_view(), name='product_create'),
    path('product_update/<int:pk>/', ProductUpdateAPIView.as_view(), name='product_update'),
    path('product_delete/<int:pk>/', ProductDeleteAPIView.as_view(), name='product_delete'),

    path('reviews/', ReviewListAPIView.as_view(), name='review_list'),
    path('reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name='review_detail'),
    path('review_create/', ReviewCreateAPIView.as_view(), name='review_create'),
    path('review_update/<int:pk>/', ReviewUpdateAPIView.as_view(), name='review_update'),
    path('review_delete/<int:pk>/', ReviewDeleteAPIView.as_view(), name='review_delete'),
]