from django.urls import path
from .views import *
from api.views import RegisterView, LoginView

urlpatterns = [
    # User URLs
    path('register/', RegisterView.as_view(), name='register'),  # API đăng ký
    path('login/', LoginView.as_view(), name='login'), # API đăng nhập

 
]