# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CartOrderItem, CartOrder

@receiver(post_save, sender=CartOrderItem)
def update_cart_total_price(sender, instance, created, **kwargs):
    if created:  # Chỉ tính toán lại nếu mục giỏ hàng được tạo mới
        cart_order = instance.order  # Lấy giỏ hàng từ CartOrderItem
        # Tính toán lại tổng giá giỏ hàng
        total_price = sum(item.quantity * item.price for item in cart_order.items.all())
        cart_order.total_price = total_price  # Cập nhật lại tổng giá
        cart_order.save()  # Lưu lại giỏ hàng đã cập nhật
