from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.password_validation import validate_password

User = get_user_model()
# Thêm vào file serializers.py (cùng với RegisterSerializer và LoginSerializer)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'phonenb']  # Loại bỏ trường nhạy cảm như password
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

# Serializer Sản phẩm:
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = ['description', 'origin', 'image', 'nutrition_info']

class ProductSerializer(serializers.ModelSerializer):
    detail = ProductDetailSerializer()  # Lồng serializer cho chi tiết sản phẩm

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity', 'category', 'detail']

    def create(self, validated_data):
        # Tách dữ liệu 'detail' từ validated_data
        detail_data = validated_data.pop('detail')
        
        # Tạo sản phẩm mới
        product = Product.objects.create(**validated_data)
        
        # Tạo chi tiết sản phẩm liên kết với sản phẩm vừa tạo
        ProductDetail.objects.create(product=product, **detail_data)
        
        return product


# Serializer CartOrder, CartOrderDetail, Payment
class CartOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartOrderItem
        fields = ['product', 'quantity', 'price']

class CartOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartOrder
        fields = ['id', 'user', 'total_price', 'status', 'created_at', 'updated_at']

class CartOrderDetailSerializer(serializers.ModelSerializer):
    items = CartOrderItemSerializer(many=True)

    class Meta:
        model = CartOrder
        fields = ['id', 'user', 'total_price', 'status', 'created_at', 'updated_at', 'items']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['order', 'payment_method', 'payment_status', 'paid_amount', 'payment_date']