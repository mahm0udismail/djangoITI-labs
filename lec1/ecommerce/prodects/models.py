from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)  # Adjust the max_length as needed

    def __str__(self):
        return self.name

class Producer(models.Model):
    name = models.CharField(max_length=255)  # Adjust the max_length as needed

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)  # Adjust the max_length as needed
    price = models.DecimalField(max_digits=10, decimal_places=2)  # For currency
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)  # For image files
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # One-to-many relationship
    producers = models.ManyToManyField(Producer)  # Many-to-many relationship

    def __str__(self):
        return self.name
