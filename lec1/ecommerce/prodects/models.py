from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)  # Adjust the max_length as needed
    price = models.DecimalField(max_digits=10, decimal_places=2)  # For currency
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)  # For image files

    def __str__(self):
        return self.name
