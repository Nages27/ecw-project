from django.db import models
from django.utils import timezone

class CustomerData(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=128)

class Cart(models.Model):
    user = models.ForeignKey(CustomerData, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(CustomerData, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, default="Pending")
    ordered_at = models.DateTimeField(auto_now_add=True)