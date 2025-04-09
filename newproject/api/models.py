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
    REQUIRED_FIELDS = ['name', 'phonenb']  # Các trường bắt buộc khi tạo user qua lệnh createsuperuser

# Model Admin
class Admin(models.Model):
    name = models.CharField(max_length=100)
    phonenb = models.CharField(max_length=20)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Model Sản Phẩm
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()  # Mô tả ngắn về sản phẩm
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='Anh/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

# Model Chi Tiết Sản Phẩm (Product Detail)
class ProductDetail(models.Model):
    product = models.OneToOneField(Product, related_name='detail', on_delete=models.CASCADE)
    detailed_description = models.TextField()  # Mô tả chi tiết sản phẩm
    ingredients = models.TextField(null=True, blank=True)  # Thành phần sản phẩm
    usage_instructions = models.TextField(null=True, blank=True)  # Hướng dẫn sử dụng
    features = models.TextField(null=True, blank=True)  # Các đặc điểm nổi bật của sản phẩm

    def __str__(self):
        return f"Details for {self.product.name}"

# Model Giỏ Hàng
class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

# Model Đơn Hàng
class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='OrderItem')
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Order {self.id} by {self.user.name}'

# OrderItem: kết nối giữa đơn hàng và sản phẩm
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
