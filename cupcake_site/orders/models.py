from django.db import models

class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    cart_items = models.TextField(default="[]")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=50, default="COD")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"