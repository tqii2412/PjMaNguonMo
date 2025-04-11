from rest_framework.views import APIView  # Import APIView cho class-based views
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer, RegisterSerializer, LoginSerializer, ProductSerializer, CartOrderSerializer, CartOrderDetailSerializer, PaymentSerializer  # Sửa lại tên file nếu cần
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model 
from rest_framework.permissions import IsAuthenticated
from .models import *

# newproject/api/views.py
User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Đăng ký thành công!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                return Response({"message": "Đăng nhập thành công!"}, status=status.HTTP_200_OK)
            return Response({"error": "Username hoặc password không đúng."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)  # Lấy người dùng theo pk
            serializer = UserSerializer(user)  # Serialize thông tin người dùng
            return Response(serializer.data, status=status.HTTP_200_OK)
        except user.DoesNotExist:
            return Response({"error": "Người dùng không tồn tại."}, status=status.HTTP_404_NOT_FOUND)
        
# View sản phẩm:
from rest_framework import viewsets
from .models import Product

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Bạn có thể lọc hoặc truy vấn các sản phẩm dựa trên một số tiêu chí, nếu cần.
        return Product.objects.all()

class CartOrderViewSet(viewsets.ModelViewSet):
    queryset = CartOrder.objects.all()
    serializer_class = CartOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartOrder.objects.filter(user=self.request.user)  # Lọc theo người dùng

class CartOrderDetailViewSet(viewsets.ModelViewSet):
    queryset = CartOrder.objects.all()
    serializer_class = CartOrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartOrder.objects.filter(id=self.kwargs['pk'], user=self.request.user)  # Lọc theo người dùng và ID đơn hàng

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)  # Lọc theo người dùng