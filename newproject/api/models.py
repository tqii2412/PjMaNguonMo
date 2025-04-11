from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Model Người Dùng
class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)  # Sử dụng username để đăng nhập
    name = models.CharField(max_length=100)  # Tên người dùng
    phonenb = models.CharField(max_length=20, unique=True)  # Số điện thoại duy nhất

    def __str__(self):
        return self.name

    # Đặt lại USERNAME_FIELD về mặc định là 'username'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'phonenb'] 

# Model Admin
class Admin(models.Model):
    name = models.CharField(max_length=100)
    phonenb = models.CharField(max_length=20)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name
# Sản phẩm:

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProductDetail(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='detail')
    description = models.TextField()
    origin = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Anh/')
    nutrition_info = models.TextField()

    def __str__(self):
        return f"Chi tiết sản phẩm {self.product.name}"

# Giỏ hàng và Đơn hàng:
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Payment(models.Model):
    order = models.OneToOneField(CartOrder, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Thanh toán {self.order.id}"