from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

# Serializer cho đăng ký
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'name', 'phonenb', 'password', 'password_confirm']

    def validate(self, data):
        # Kiểm tra xem password và password_confirm có khớp nhau không
        if 'password_confirm' in data and data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Mật khẩu và xác nhận mật khẩu không khớp."})
        return data

    def create(self, validated_data):
        # Loại bỏ password_confirm vì không cần lưu vào model
        validated_data.pop('password_confirm')
        # Tạo user mới với mật khẩu đã mã hóa
        user = User.objects.create_user(
            username=validated_data['username'],
            name=validated_data['name'],
            phonenb=validated_data['phonenb'],
            password=validated_data['password']
        )
        return user

# Serializer cho đăng nhập
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Cần nhập cả username và password.")

        return data

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'