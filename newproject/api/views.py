from rest_framework.views import APIView  # Import APIView cho class-based views
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterSerializer, LoginSerializer  # Sửa lại tên file nếu cần
from django.contrib.auth import authenticate
# newproject/api/views.py

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