from django.db import models
from PIL import Image as PILImage
import io
from django.core.files.base import ContentFile
from django.utils import timezone
from accounts.models import Account
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    

class DetailCategory(models.Model):
    name = models.CharField(max_length=255)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='detail_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class Brand(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
    
class Discount(models.Model):
    percentage=models.DecimalField(max_digits=5,decimal_places=2)
    
    def __str__(self) -> str:
        return str(f'{self.percentage}%')
    
class Product(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    price=models.DecimalField(decimal_places=2,max_digits=10)
    stock_amount=models.IntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_category=models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name='products')
    detail_category=models.ForeignKey(DetailCategory,on_delete=models.CASCADE,null=True,blank=True)
    primary_image=models.ImageField(upload_to='images/')
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,default="General") 
    discount=models.ForeignKey(Discount,on_delete=models.SET_NULL,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = PILImage.open(self.primary_image.path)
        img = img.resize((540, 600))

        img_io = io.BytesIO()
        original_format = self.primary_image.name.split('.')[-1].upper()
        img.save(img_io, format=original_format, quality=85)
        img_file = ContentFile(img_io.getvalue(), name=self.primary_image.name)
        self.primary_image.save(self.primary_image.name, img_file, save=False)
        super().save(*args, **kwargs)
    
    @property
    def variants(self):
        return self.variants.all()
    
    @property
    def discountedPrice(self):
        if self.discount:
            discount_price=(self.discount.percentage /100) * self.price
            return self.price - discount_price
        return self.price
    
    @property
    def is_new(self):
        return (timezone.now() - self.created_at).days <= 15
    
    def in_stock(self):
        return self.stock_amount > 0
    
    def __str__(self) -> str:
        return self.name
    
    
class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
class Variantion(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.name
    
class VariantValue(models.Model):
    variation=models.ForeignKey(Variantion,on_delete=models.CASCADE,related_name='values')
    value=models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return f"{self.variation.name}:{self.value}"
    
class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    value = models.ForeignKey(VariantValue, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.value} {self.product.name}"
    
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='wishlists')
    products=models.ForeignKey(Product,on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'products')
    
    
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def total_price(self):
        return self.product.price * self.quantity
 
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    
