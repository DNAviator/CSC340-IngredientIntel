from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    """
    Search field for products in Admin
    """
    list_display = ('name', 'producing_company')
    search_fields = ['name']

admin.site.register(Ingredient)
admin.site.register(Company)
admin.site.register(Product, ProductAdmin)
admin.site.register(SCINote)
admin.site.register(Profile)