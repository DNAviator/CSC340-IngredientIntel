from django.db import models
from django.db.models import Func, F
from django.db.models.functions import Cast

from django.conf import settings
import os

class Levenshtein(Func):
    """
    The levenshtien search function from the django.db.models Func

    parameters:
        expression: 
        search_term: The user's search query

        **extras
    
    """
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
    Represents an individual ingredient with detailed information.

    This model stores data related to ingredients used in products, including their unique name,
    intended purpose, any associated warnings, and related notes.

    Attributes:
        name (models.CharField): The unique name of the ingredient.
        purpose (models.TextField): The intended use or role of the ingredient in products.
        warnings (models.TextField): Any warnings related to the ingredient. This field is optional.
        notes (models.ManyToManyField): A many-to-many relationship to the SCINote model, allowing for the association of multiple notes with a single ingredient. This field is optional.
    """
    name = models.CharField(max_length=255, unique=True)
    purpose = models.TextField()
    warnings = models.TextField(blank=True)
    notes = models.ManyToManyField('SCINote', related_name='notes', blank=True)

    # general search function
    def search_db(self, search_criteria, query):
        # ranks all results with Levenshtein distance function to query
        result = Ingredient.objects.annotate(
            rank = Cast(Levenshtein(F(search_criteria), query), output_field=models.IntegerField())
        ).order_by('rank')

        return result

    def __str__(self):
        """Return a human-readable representation of the ingredient object."""
        return self.name


class Company(models.Model):
    """
    Represents a company that produces products.

    The Company model includes information about companies such as their unique name,
    the date they were founded, and any products they produce. It also allows for the storage
    of additional textual notes.

    Attributes:
        name (models.CharField): The unique name of the company.
        products (models.ManyToManyField): A many-to-many relationship with the Product model, representing the products produced by the company. This field is optional.
        date_founded (models.DateField): The date when the company was founded.
        notes (models.TextField): Additional textual notes about the company. This field is optional.
    """
    name = models.CharField(max_length=255, unique=True)
    products = models.ManyToManyField('Product', related_name='products', blank=True)
    date_founded = models.DateField()
    notes = models.TextField(blank=True)

    # general search function
    # def search_db(self, query):
    #     # ranks all results with Levenshtein distance function to query
    #     result = Company.objects.annotate(
    #         rank=Cast(Levenshtein(Company.name, query), output_field=models.IntegerField())
    #     ).order_by('rank')
    #     return result
    # general search function
    def search_db(self, search_criteria, query):
        # ranks all results with Levenshtein distance function to query
        result = Company.objects.annotate(
            rank = Cast(Levenshtein(F(search_criteria), query), output_field=models.IntegerField())
        ).order_by('rank')

        return result

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        """Return a human-readable representation of the company object."""
        return self.name


class Product(models.Model):
    """
    Represents a product with associated details.

    The Product model contains information about various products, including their name,
    producing company, ingredients, and any warnings or additional notes that may be relevant.

    Attributes:
        name (models.CharField): The name of the product.
        producing_company (models.ForeignKey): A reference to the Company model, representing the company that produces the product. On deletion of a company, all associated products are also deleted.
        ingredients (models.ManyToManyField): A many-to-many relationship with the Ingredient model, representing the ingredients contained in the product.
        warnings (models.TextField): Any warnings associated with the product. This field is optional.
        notes (models.TextField): Additional notes or comments about the product from the producing company. This field is optional.
    """
#will implement later
    #def find_product(self, query) :


    # # general search function
    # def search_db(self, query):
    #     # ranks all results with Levenshtein distance function to query
    #     result = Product.objects.annotate(
    #         rank= Cast(Levenshtein(Product.name, query), output_field=models.IntegerField())
    #     ).order_by('rank')
        
    #     return result
        # general search function

    def search_db(self, search_criteria, query):
        # ranks all results with Levenshtein distance function to query
        result = Product.objects.annotate(
            rank = Cast(Levenshtein(F(search_criteria), query), output_field=models.IntegerField())
        ).order_by('rank')

        return result


    name = models.CharField(max_length=255)
    producing_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)
    warnings = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    item_id = models.TextField(blank=True)

    def __str__(self):
        """Return a human-readable representation of the product object."""
        return self.name

class SCINote(models.Model):
    """
    Data describing a scientific note applied to a specific ingredient

    Attributes:
        researcher_names(models.TextField): The name(s) of the contributing author(s)
        institution_name(models.TextField): The name of the institutional sponser of the note, this field is optional
        notes_content(models.TextField): The description and details of the research note (at the very least the abstract)
        citations(models.TextField): Any citations to the full paper or other important resources, if the article is completely included no reference is needed, this field is optional
        ingredient(ForeignKey): A reference to the Ingredient model which the note is about, if that ingredient for any reason was deleted all related notes will be deleted
    """
    researcher_names = models.TextField()
    institution_name = models.TextField(blank=True)
    notes_content = models.TextField()
    citations = models.TextField(blank=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        """Return a human-readable representation of the SCINote object."""
        return f"Related ingredient: {self.ingredient}\nAuthors: {self.researcher_names}\nInstitutional Sponsor: {self.institution_name}\nNote: {self.notes_content}"

    class Meta:
        verbose_name = "Scientific Notes"
        verbose_name_plural = "Scientific Notes"
    

class ImageModel(models.Model):
    """
    Model for intaking images

    Attributes:
        img(model.ImageField): Image taken from user
    """
    img = models.ImageField(upload_to = "images/")

    def __str__(self):
        return self.title