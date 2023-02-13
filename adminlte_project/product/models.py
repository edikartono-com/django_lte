from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    picture = models.ImageField(upload_to='images/category', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
         return self.name or ''

class Brand(models.Model):
    name = models.CharField(max_length=200, null=True, default='None')

    def __str__(self):
         return self.name or ''

# Create your models here.
class Product(models.Model):
    class Status(models.TextChoices):
        DISABLE = 'DI', 'Disable'
        ENABLE = 'EN', 'Enable'

    sku = models.CharField(max_length=200, null=True, unique=True)
    name = models.CharField(max_length=200, null=True)
    featured_image = models.ImageField(upload_to="featured_image_path", null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE, related_name='brands_product', blank=True, null=True )
    bom_file = models.FileField(upload_to='file', null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                                choices=Status.choices,
                                default=Status.ENABLE)

    class Meta:
        ordering = ['-created_at']
        indexes = [
        models.Index(fields=['-created_at']),
        ]
        # unique_together = ('sku',)

    def __str__(self):
        return self.name or ''

class AmbienceImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ambience_image')
    image = models.ImageField(upload_to = 'ambience_image', null=True)

class SpecificationImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='spec_image')
    image = models.ImageField(upload_to = 'specification_image', null=True)

class TechnicalImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='technical_image')
    image = models.ImageField(upload_to = 'technical_image', null=True)