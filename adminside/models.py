from typing import Any
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save,post_save
from django.utils.text import slugify
from django.dispatch import receiver
from django.contrib.auth.models import User





class nav_slider(models.Model):
    title=models.CharField(max_length=255)
    image=models.ImageField(upload_to='image/slider')
    discount=models.PositiveBigIntegerField(default=0,null=True)
    link=models.CharField(max_length=255,default='#')

    def __str__(self):
        return self.title[:50]
    

class maincategory(models.Model):
    title=models.CharField(max_length=255)
    

    def __str__(self):
        return self.title[:50]
    
class category(models.Model):
    title = models.CharField(max_length=255, unique=True)  # Added unique=True
    image = models.ImageField(upload_to='image/maincategory')
    maincategory = models.ForeignKey('maincategory', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title[:50]
    
class subcategory(models.Model):
    title=models.CharField(max_length=255)
    category=models.ForeignKey(category,null=True,on_delete=models.CASCADE)


    def __str__(self):
        return self.title 
    


class product(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(category, null=True, on_delete=models.DO_NOTHING)
    price = models.PositiveBigIntegerField(default=0, null=True)
    discount = models.PositiveBigIntegerField(default=0, null=True)
    Featured_image = models.ImageField(upload_to='featured_images/', null=True, blank=True)
    total = models.PositiveBigIntegerField(default=0, null=True)
    description = RichTextField(null=True, blank=True)
    product_information = RichTextField(null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    additional_info = RichTextField(null=True, blank=True)
    
    # New fields for filtering
    color = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.title[:50]
    
class AdditionalImage(models.Model):
    product = models.ForeignKey(product, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='additional_images/')

    def __str__(self):
        return f"{self.product.title} - Additional Image"

@receiver(pre_save,sender=product)
def generate_slug(sender,instance,*args,**wargs):
    if not instance.slug:
        base_slug=slugify(instance.title)
        unique_slug= base_slug
        while product.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{base_slug}-{instance.id}'
        instance.slug=unique_slug



    
    


class offers(models.Model):
    title=models.CharField(max_length=255,null=True,blank=True)
    discount=models.PositiveBigIntegerField(default=True,null=True)
    image=models.ImageField(upload_to='image/offer')


#useraddressarea

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.state}, {self.country}"
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} - {self.order.id}"



    
    






    

    

    
