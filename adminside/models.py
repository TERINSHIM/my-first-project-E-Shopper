from typing import Any
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save,post_save
from django.utils.text import slugify
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone





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
    title = models.CharField(max_length=255, unique=True)  
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

    
    colors = models.ManyToManyField('Color', blank=True, related_name="products")
    sizes = models.ManyToManyField('Size', blank=True, related_name="products")

    def __str__(self):
        return self.title[:50]


class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name
    
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
    


    
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.product.title} - {self.color} - {self.size} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
    
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        return self.is_active and self.valid_from <= timezone.now() <= self.valid_to
    


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Return Requested', 'Return Requested'),
        ('Returned', 'Returned'),
        ('Return Rejected', 'Return Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    order_date = models.DateTimeField(auto_now_add=True)
    payment = models.OneToOneField('Payment', on_delete=models.SET_NULL, null=True, blank=True)
    
    return_requested = models.BooleanField(default=False)  # New field to track return request

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


   

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)

    @property
    def discounted_price(self):
        """Returns the price after applying product-level discount."""
        discount_amount = self.product.discount or 0  
        return max(self.price - discount_amount, 0)  

    def __str__(self):
        return f"{self.product.title} - {self.color} - {self.size} - Order {self.order.id}"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.user.username} - Order ID: {self.razorpay_order_id}"
    

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=(('CREDIT', 'Credit'), ('DEBIT', 'Debit')))
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"



class Sale(models.Model):
    product = models.ForeignKey(product, related_name='sales', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    sale_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.product.title} - {self.quantity} units"
    



    



    
    






    

    

    
