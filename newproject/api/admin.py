from django.contrib import admin
from .models import User, Admin, Product, ProductDetail, CartOrder, CartOrderItem, Payment

# Đăng ký mô hình User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'phonenb', 'is_active', 'is_staff')
    search_fields = ('username', 'name', 'phonenb')
    list_filter = ('is_active', 'is_staff')
    ordering = ('username',)
    fieldsets = (
        (None, {
            'fields': ('username', 'name', 'phonenb', 'password')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
    )

# Đăng ký mô hình Admin
@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'phonenb')
    search_fields = ('name', 'phonenb')

# Đăng ký mô hình Product
class ProductDetailInline(admin.StackedInline):
    model = ProductDetail
    extra = 1  # Số dòng trống để thêm chi tiết sản phẩm mới

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    search_fields = ('name', 'category')
    list_filter = ('category',)
    ordering = ('name',)
    inlines = [ProductDetailInline]

# Đăng ký mô hình ProductDetail
@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('product', 'origin', 'description')
    search_fields = ('product__name', 'origin')
    list_filter = ('product__category',)

# Đăng ký mô hình CartOrder
@admin.register(CartOrder)
class CartOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'status')
    list_filter = ('status',)
    ordering = ('-created_at',)

# Đăng ký mô hình CartOrderItem
@admin.register(CartOrderItem)
class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')
    list_filter = ('order__status',)

# Đăng ký mô hình Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'payment_status', 'paid_amount', 'payment_date')
    search_fields = ('order__id', 'payment_method', 'payment_status')
    list_filter = ('payment_status',)
    ordering = ('-payment_date',)
