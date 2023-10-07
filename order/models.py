from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class paymentMode(models.TextChoices):
    COD='COD'
    CARD='CARD'

class payment(models.TextChoices):
    PAID='PAID'
    UNPAID='UNPAID'
class orderstatus(models.TextChoices):
    PROCESSING='Processing'
    SHIPED='Shipped'
    DELIVERED='Deliverd'

# Create your models here.
class Order(models.Model):
    street=models.CharField(max_length=500,default="",blank=False)
    city=models.CharField(max_length=100,default="",blank=False)
    state=models.CharField(max_length=100,default="",blank=False)
    zip_code=models.CharField(max_length=100,default="",blank=False)
    phone_no=models.CharField(max_length=100,default="",blank=False)
    country=models.CharField(max_length=100,default="",blank=False)
    total_amount=models.IntegerField(default=0)
    payment_status=models.CharField(
        max_length=20,
        choices=payment.choices,
        default=payment.UNPAID
    )
    order_status=models.CharField(
        max_length=50,
        choices=orderstatus.choices,
        default=orderstatus.PROCESSING
    )
    payment_mode=models.CharField(
        max_length=50,
        choices=paymentMode.choices,
        default=paymentMode.COD
    )
    User=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.id)
    

class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True,related_name="orderitems")
    name=models.CharField(max_length=200,default="",blank=False)
    quantity=models.IntegerField(default=1)
    price=models.DecimalField(max_digits=7,decimal_places=2,blank=False)


    def __str__(self):
        return str(self.name)

