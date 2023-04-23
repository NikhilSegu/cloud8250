from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

# Create your models here.


def userDirectoryPath(uname, file):
	return 'user_{0}/{1}'.format(uname, file)

class FileUpload(models.Model):

	#uname = models.CharField(default='', max_length=100)

	file = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['txt'])])

	
class Household(models.Model):
	#households_csvfile = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'])])
	HSHD_NUM = models.IntegerField(default = 1, blank=True, primary_key=True)
	L = models.CharField(max_length=10)
	AGE_RANGE = models.CharField(max_length=100)
	MARITAL = models.CharField(max_length=100)
	INCOME_RANGE = models.CharField(max_length=100)
	HOMEOWNER = models.CharField(max_length=100)
	HSHD_COMPOSITION = models.CharField(max_length=100)
	HH_SIZE = models.IntegerField(default=1, blank=True)
	CHILDREN = models.IntegerField(default=1, blank=True)

class Product(models.Model):
	#products_csvfile = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'])])
	PRODUCT_NUM = models.IntegerField(default=1, blank=True, primary_key = True)
	DEPARTMENT = models.CharField(max_length=100)
	COMMODITY = models.CharField(max_length=100)
	BRAND_TY = models.CharField(max_length=100)
	NATURAL_ORGANIC_FLAG = models.CharField(max_length=100)

	
class Transaction(models.Model):
	#transactions_csvfile = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'])])
	BASKET_NUM = models.IntegerField(default=-1, blank=True, null=True)
	HSHD_NUM = models.ForeignKey(Household, on_delete = models.CASCADE)
	PURCHASE = models.CharField(max_length=100)
	PRODUCT_NUM = models.ForeignKey(Product, on_delete = models.CASCADE)
	SPEND = models.DecimalField(default=0.00, decimal_places=2, max_digits=7)
	UNITS = models.IntegerField(default=0, blank=True, null=True)
	STORE_R = models.CharField(max_length=100)
	WEEK_NUM = models.IntegerField(default = 0, blank=True, null=True)
	YEAR = models.IntegerField(default = 2000, blank=True, null=True)

