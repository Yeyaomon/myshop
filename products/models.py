from django.db import models

# Create your models here.
# products/models.py
class Product(models.Model):
    # Cargo's name
    name        = models.CharField(max_length=200)
    # Cargo's overall
    description = models.TextField(blank=True)
    # Cargo's price
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    # Cargo's stock
    stock       = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name