from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Company)
admin.site.register(Product)
admin.site.register(SCINote)