from django.db import models
from django.db.models import Func

class Levenshtein(Func):
    template = "%(function)s(%(expressions)s, '%(search_term)s')"
    function = "levenshtein"

    def __init__(self, expression, search_term, **extras):
        super(Levenshtein, self).__init__(
            expression,
            search_term=search_term,
            **extras
        )


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
    products = models.ManyToManyField('Product', related_name='companies', blank=True)
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

# class Researcher(models.Model):
#     """
#     Data
#     """
#     name = models.CharField(max_length=255)
#     notes = models.ManyToManyField(Ingredient)
    