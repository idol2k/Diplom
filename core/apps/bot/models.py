from django.db import models

class pizza(models.Model):
    id = models.AutoField(primary_key=True)
    pizza_name = models.TextField()
    size = models.TextField()
    price = models.TextField()
