from django.urls import path, include
from .views import *
from api.views import RegisterView, LoginView,UserListView, UserDetailView
from rest_framework.routers import DefaultRouter
from api.views import ProductViewSet, CartOrderViewSet, CartOrderDetailViewSet, PaymentViewSet, CartOrderItemViewSet # Thêm import cho ProductViewSet
from rest_framework_simplejwt import views as jwt_views


# Tạo router và đăng ký ViewSet cho sản phẩm
router = DefaultRouter()
router.register(r'products', ProductViewSet)  # Đăng ký ViewSet cho sản phẩm
router.register(r'cartorders', CartOrderViewSet, basename='cartorder')  # Đăng ký ViewSet cho giỏ hàng với basename 'cartorder'
# Thay đổi URL của CartOrderDetailViewSet
router.register(r'cartorders/<int:order_id>/details', CartOrderDetailViewSet, basename='cartorderdetail')
router.register(r'cartorderitems', CartOrderItemViewSet, basename='cartorderitem')
router.register(r'payments', PaymentViewSet)  # Đăng ký ViewSet cho thanh toán


urlpatterns = [
    # User URLs
    path('register/', RegisterView.as_view(), name='register'),  # API đăng ký
    path('login/', LoginView.as_view(), name='login'), # API đăng nhập
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),


    # JWT Authentication URLs (Đăng nhập và làm mới token)
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Đăng nhập và nhận JWT token
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # Làm mới JWT token   
    # Sản phẩm URLs
    path('', include(router.urls)),  # Thêm các URL từ router cho sản phẩm

    
]