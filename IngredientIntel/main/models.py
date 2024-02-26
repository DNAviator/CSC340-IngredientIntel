from django.db import models

# Create your models here.
class Ingredient(models.Model):
    """
    Ingredients data table includes all the ingredient data
    """
    name = models.CharField(max_length=255, unique=True)
    purpose = models.TextField()
    warnings = models.TextField(blank=True)
    notes = models.TextField(blank=True)

class Company(models.Model):
    """
    Company data table includes all the company data
    """
    name = models.CharField(max_length=255, unique=True)
    products = models.ManyToManyField('Product', related_name='companies')
    date_founded = models.DateField()
    notes = models.TextField(blank=True)


class Product(models.Model):
    """
    Products data table includes all the product data
    """
    name = models.CharField(max_length=255)
    producing_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)
    warnings = models.TextField(blank=True)
    notes = models.TextField(blank=True)