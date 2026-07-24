from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Store, Product, Review
from .serializers import (CategoryListSerializers, CategoryDetailSerializers,
                          StoreListSerializers, StoreDetailSerializers, StoreEditSerializers,
                          ProductListSerializers, ProductDetailSerializers, ProductEditSerializers,
                          ReviewListSerializers, ReviewDetailSerializers, ReviewEditSerializers)
from .filters import StoreFilter, ProductFilter
from .pagination import StorePagination, ProductPagination
from .permissions import (IsStoreOwner, IsStoreOwnerObject, IsOwnerOfStore,
                          IsSimpleUser, IsReviewOwner)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializers


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializers


class StoreListAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = StoreFilter
    search_fields = ['store_name', 'description']
    ordering_fields = ['store_name']
    pagination_class = StorePagination


class StoreDetailAPIView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializers


class StoreCreateAPIView(generics.CreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreEditSerializers
    permission_classes = [IsStoreOwner]

    def perform_create(self, serializer):
        serializer.save(store_owner=self.request.user.id)


class StoreUpdateAPIView(generics.UpdateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreEditSerializers
    permission_classes = [IsAuthenticated, IsStoreOwnerObject]


class StoreDeleteAPIView(generics.DestroyAPIView):
    queryset = Store.objects.all()
    permission_classes = [IsAuthenticated, IsStoreOwnerObject]


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    ordering_fields = ['price']
    pagination_class = ProductPagination


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializers


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductEditSerializers
    permission_classes = [IsAuthenticated, IsOwnerOfStore]


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductEditSerializers
    permission_classes = [IsAuthenticated, IsStoreOwnerObject]


class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsStoreOwnerObject]


class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializers


class ReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializers


class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewEditSerializers
    permission_classes = [IsSimpleUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.id)


class ReviewUpdateAPIView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewEditSerializers
    permission_classes = [IsAuthenticated, IsReviewOwner]


class ReviewDeleteAPIView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated, IsReviewOwner]
