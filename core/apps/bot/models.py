from django.db import models

class Pizza(models.Model):
    pepperoni = models.CharField(max_length=100)
    gavaii = models.CharField(max_length=100)
    chicken = models.CharField(max_length=100)
    burger = models.CharField(max_length=100)

class Size(models.Model):
    small = models.IntegerField()
    medium = models.IntegerField()
    large = models.IntegerField()

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16)
    password = models.CharField(max_length=32)
    token = models.TextField()