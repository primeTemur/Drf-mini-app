from django.urls import path
from .import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('products/',views.ProductListAPIView.as_view()),
    path('products/info/',views.ProductInfoAPIView.as_view()),
    path('products/<int:product_id>/',views.ProductDetailAPIView.as_view(),name="product-detail"),
    path('users/',views.UserListView.as_view()),
    # path('orders/',views.OrderListAPIView.as_view()),
    # path('users-orders/',views.UserOrderListAPIView.as_view()),

]

router=DefaultRouter()
router.register('orders',views.OrderViewSet)
urlpatterns+=router.urls


