from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete

# Create your models here.

class Category(models.TextChoices):
    ELECTRONICS='Electronics'
    LAPTOP='Laptop'
    ARTS='Arts'
    FOOD='Food'
    HOME='Home'
    KITCHEN='Kitchen'

class Product(models.Model):
    Name=models.CharField(max_length=200,default="",blank=False)
    Description=models.TextField(max_length=1000,default="",blank=False)
    Price=models.DecimalField(max_digits=7,decimal_places=2,default=0)
    Brand=models.CharField(max_length=200,default="",blank=False)
    Category=models.CharField(max_length=30,choices=Category.choices)
    Rating=models.DecimalField(max_digits=3,decimal_places=2,default=0)
    Stock=models.IntegerField(default=0)
    User=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    CreatedAt=models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.Name
    
class ProductImages(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,related_name="images")
    Image=models.ImageField(upload_to='products')
@receiver(post_delete,sender=ProductImages)
def auto_delete_file(sender,instance,**kwargs):
    if instance.Image:
        instance.Image.delete(save=False)


class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,related_name="review")
    User=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    rating=models.IntegerField(default=0)
    comment=models.TextField(default="",blank=False)
    CreatedAt=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.comment)
    







