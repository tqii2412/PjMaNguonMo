from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.db.models import F

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
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = CartOrderItem
        fields = ['order', 'product', 'product_detail', 'quantity', 'price']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Số lượng phải lớn hơn 0.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Giá sản phẩm phải lớn hơn 0.")
        return value

    def create(self, validated_data):
        cart_order = validated_data['order']
        product = validated_data['product']
        quantity = validated_data['quantity']
        price = product.price  # Lấy giá sản phẩm từ product

        # Cập nhật tổng giá giỏ hàng
        cart_order.total_price += quantity * price
        cart_order.save()

        return super().create(validated_data)

    
#CartOrderSerializer

from rest_framework.exceptions import ValidationError

class CartOrderSerializer(serializers.ModelSerializer):
    items = CartOrderItemSerializer(many=True)  # Lồng CartOrderItemSerializer để trả về các mục giỏ hàng

    class Meta:
        model = CartOrder
        fields = ['id', 'user', 'total_price', 'status', 'created_at', 'updated_at', 'items']  # Bao gồm trường 'items'

    def create(self, validated_data):
        user_id = validated_data.get('user')
        total_price = validated_data.get('total_price', 0)

        # Kiểm tra xem user có tồn tại không
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError("Người dùng không tồn tại.")

        # Tạo giỏ hàng mới
        cart_order = CartOrder.objects.create(user=user, total_price=total_price, status='pending')

        # Cập nhật lại tổng giá giỏ hàng nếu cần
        items = CartOrderItem.objects.filter(order=cart_order)  # Lấy các mục trong giỏ hàng
        cart_order.total_price = sum(item.quantity * item.price for item in cart_order.items.all()) or 0  # Tránh giá trị None
        cart_order.save()

        return cart_order



class CartOrderDetailSerializer(serializers.ModelSerializer):
    items = CartOrderItemSerializer(many=True)

    class Meta:
        model = CartOrder
        fields = ['id', 'user', 'total_price', 'status', 'created_at', 'updated_at', 'items']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['order', 'payment_method', 'payment_status', 'paid_amount', 'payment_date']