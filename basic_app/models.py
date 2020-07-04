from django.db import models

# Create your models here.
class Product(models.Model):

    product_name = models.CharField(max_length=100)
    product_url = models.URLField()
    target_price = models.PositiveIntegerField()
    your_email = models.EmailField()

    def __str__(self):
        return self.product_name;
