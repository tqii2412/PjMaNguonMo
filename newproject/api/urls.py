from django.urls import path, include
from .views import *
from api.views import RegisterView, LoginView,UserListView, UserDetailView
from rest_framework.routers import DefaultRouter
from api.views import ProductViewSet, CartOrderViewSet, CartOrderDetailViewSet, PaymentViewSet # Thêm import cho ProductViewSet



# Tạo router và đăng ký ViewSet cho sản phẩm
router = DefaultRouter()
router.register(r'products', ProductViewSet)  # Đăng ký ViewSet cho sản phẩm
router.register(r'cartorders', CartOrderViewSet, basename='cartorder')  # Đăng ký ViewSet cho giỏ hàng với basename 'cartorder'
router.register(r'cartorders/(?P<order_id>\d+)/details', CartOrderDetailViewSet, basename='cartorderdetail')  # Đăng ký ViewSet cho chi tiết giỏ hàng với basename 'cartorderdetail'
router.register(r'payments', PaymentViewSet)  # Đăng ký ViewSet cho thanh toán


urlpatterns = [
    # User URLs
    path('register/', RegisterView.as_view(), name='register'),  # API đăng ký
    path('login/', LoginView.as_view(), name='login'), # API đăng nhập
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),


    # Sản phẩm URLs
    path('', include(router.urls)),  # Thêm các URL từ router cho sản phẩm
]