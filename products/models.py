from django.db import models
from accounts.models import User
from django.utils import timezone

Categories = (
    ("Cellphones and Tablets", "Cellphones and Tablets"),
    ("Laptops and Computers", "Laptops and Computers"),
    ("Electronic Gadgets", "Electronic Gadgets"),
    ("Tech Accessories", "Tech Accessories"),
    ("Electrical Appliances", "Electrical Appliances"),
    ("Shoes and Footware", "Shoes and Footware"),
    ("Watches and Accessories", "Watches and Accessories"),
    ("Beauty and Cosmetics", "Beauty and Cosmetics"),
    ("Books and Toys", "Books and Toys"),
    ("Others", "Others"),
)

class ProductCategory(models.Model):
    image = models.ImageField(upload_to='category_images/')
    category = models.CharField(max_length=100,unique=True,choices=Categories)

    def __str__(self):
        return f"{self.category}"

class Products(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)
    is_live = models.BooleanField(default=True)
    highest_bid = models.FloatField(default=0.0)
    category = models.ManyToManyField(ProductCategory, default="", blank=False)
    location = models.CharField(max_length=255, blank=False)
    image = models.ImageField(upload_to='product_images/')
    file1 = models.FileField(upload_to='product_files/', blank=True)
    file2 = models.FileField(upload_to='product_files/', blank=True)
    file3 = models.FileField(upload_to='product_files/', blank=True)
    file4 = models.FileField(upload_to='product_files/', blank=True)
    file5 = models.FileField(upload_to='product_files/', blank=True)
    file6 = models.FileField(upload_to='product_files/', blank=True)
    file7 = models.FileField(upload_to='product_files/', blank=True)
    file8 = models.FileField(upload_to='product_files/', blank=True)
    file9 = models.FileField(upload_to='product_files/', blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    time_posted = models.TimeField(auto_now_add=True)
    shipping_charges = models.FloatField(blank=False)
    returns = models.IntegerField(blank=False)
    specifications = models.CharField(max_length=4096)
    description = models.CharField(max_length=512)
    base_price = models.FloatField(blank=False)
    deadline = models.DateField(blank=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.deadline < timezone.now().date():
            self.is_live = False
        super().save(*args, **kwargs)

class Bidding(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {self.user.username}"
