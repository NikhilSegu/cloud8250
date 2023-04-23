from django.contrib import admin
from .models import FileUpload, Household, Product, Transaction

# Register your models here.

models = [FileUpload, Household, Product, Transaction]

admin.site.register(models)