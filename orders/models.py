from django.db import models
from django.conf import settings
from products.models import Product
from django.conf import settings

# Create your models here.
# orders/models.py

# Order and Dashboard Function
class Order(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date   = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price    = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

# Cart Function
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

