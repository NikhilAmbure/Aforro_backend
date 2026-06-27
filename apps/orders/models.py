from django.db import models
from apps.stores.models import Store
from apps.products.models import Product
from django.core.validators import MinValueValidator


class Order(models.Model):
    
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        REJECTED = 'REJECTED', 'Rejected'
    
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)\
    
    def __str__(self):
        return f"Order #{self.id} - {self.status}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_requested = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity_requested} x {self.product.title} (Order #{self.order.id})"