from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CategoryProduct(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"Category: {self.name} || Description: {self.description}"


class SizeProduct(models.Model):
    size = models.CharField(max_length=20)

    def __str__(self):
        return f"Size: {self.size}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=True)
    image_url = models.CharField(max_length=255, null=True)
    category_id = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Product: {self.name} || Label: {self.label} || Price: {self.price} || {self.category_id}"


class InventoryProduct(models.Model):
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id_size = models.ForeignKey(SizeProduct, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True) 

    def __str__(self):
        return f"{self.id_product.name} || {self.id_size} || Quantity: {self.quantity}"


class RateProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product: {self.product.name} || User: {self.user} || Rate: {self.rate} || Date: {self.date.strftime('%d/%m/%Y')}"
