from django.db import models

class pizza(models.Model):
    id = models.AutoField(primary_key=True)
    pizza_name = models.TextField()
    size = models.TextField()
    price = models.TextField()
    ingredients = models.TextField()

class orders(models.Model):
    user_id = models.TextField()
    pizza_name = models.TextField()
    product_price = models.TextField()
    id = models.AutoField(primary_key=True)
    size = models.TextField()
