from django.urls import path
from .views import *
from api.views import RegisterView, LoginView,UserListView, UserDetailView

urlpatterns = [
    # User URLs
    path('register/', RegisterView.as_view(), name='register'),  # API đăng ký
    path('login/', LoginView.as_view(), name='login'), # API đăng nhập
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]