from django.db.models.aggregates import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from api.serializers import (
    ProductSerializer,OrderSerializer,
    ProductInfoSerializer,OrderCreateSerializer,
    UserSerializer
    )
from api.models import Product,Order,User
from rest_framework.decorators import APIView, api_view,action
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)

from rest_framework.views import APIView
from rest_framework import filters
from api.filters import ProductFilter,InStockFilterBackend,OrderFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from rest_framework import viewsets

from rest_framework.throttling import ScopedRateThrottle


class ProductListAPIView(generics.ListCreateAPIView):
    throttle_scope='products'
    throttle_classes=[ScopedRateThrottle]
    queryset=Product.objects.order_by('pk')
    serializer_class=ProductSerializer
    filterset_class=ProductFilter
    filter_backends=[
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend
    ]
    ordering_fields=['price','name','stock']
    search_fields=['name','description']
    pagination_class=LimitOffsetPagination
    # pagination_class.page_size=2
    # pagination_class.page_query_param='pagenum'
    # pagination_class.page_size_query_param='size'
    # pagination_class.max_page_size=4

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes=[IsAdminUser] 
        return super().get_permissions()



class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_url_kwarg='product_id'

    def get_permissions(self):
            if self.request.method in ['PUT','DELETE','PATCH']:
                self.permission_classes=[IsAdminUser] 
            return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    throttle_scope='orders'
    queryset=Order.objects.prefetch_related('items__product')
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]
    pagination_class=None
    filterset_class=OrderFilter
    filter_backends=[DjangoFilterBackend]

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        if self.action=='create' or self.action=='update':
            return OrderCreateSerializer(*args,**kwargs)
        return super().get_serializer_class()

    def get_queryset(self):
        qs=super().get_queryset()
        if not self.request.user.is_staff:
            qs=qs.filter(user=self.request.user)
        return qs



class OrderListAPIView(generics.ListAPIView):
    queryset=Order.objects.prefetch_related('items__product')
    serializer_class=OrderSerializer
    
class UserOrderListAPIView(generics.ListAPIView):
    queryset=Order.objects.prefetch_related('items__product')
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        qs=super().get_queryset()
        return qs.filter(user=self.request.user)
    
class ProductInfoAPIView(APIView):
    pass
    


class UserListView(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    pagination_class=None
