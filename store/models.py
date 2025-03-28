from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=200)
    slug=models.SlugField(max_length=210,unique=True)
    author = models.CharField(max_length=200, default='Not defined')
    description = models.TextField(max_length=3000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    quantity   	 = models.IntegerField(default=0)


    def save(self, *args, **kwargs):
        # Generate the slug from the title
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except ValueError:
            url = ''
        return url

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)
    # order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(default=True)  # New field indicating the default address


    def __str__(self):
        return self.address



class Order(models.Model):
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        return any(item.product.digital is False for item in self.orderitem_set.all())

    @property
    def get_cart_total(self):
        return sum(item.get_total() for item in self.orderitem_set.all())

    @property
    def get_cart_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        return self.product.price * self.quantity




class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.quantity} x {self.product.name}"