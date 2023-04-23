from django.shortcuts import render, redirect
from django.http import HttpResponse
from . forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import FileUpload, Product, Transaction, Household
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
import os, mimetypes
import csv

def home(request):
	allUsers = User.objects.all()
	#print(request.user.id)


	if request.method=='POST':

		households = request.FILES['households']
		products = request.FILES['products']
		transactions = request.FILES['transactions']

		if households and products and transactions:

			Transaction.objects.all().delete()
			Household.objects.all().delete()
			Product.objects.all().delete()
			#Transaction.objects.all().delete()

			decoded_households = households.read().decode('utf-8').splitlines()
			reader1 = csv.DictReader(decoded_households)
			for row in reader1:
				#print(row)

				row = {k.strip():v for k, v in row.items()}

				hargs = {

					'HSHD_NUM': row['HSHD_NUM'],
					'L': row['L'],
					'AGE_RANGE': row['AGE_RANGE'],
					'MARITAL': row['MARITAL'],
					'INCOME_RANGE': row['INCOME_RANGE'],
					'HOMEOWNER': row['HOMEOWNER'],
					'HSHD_COMPOSITION': row['HSHD_COMPOSITION'],
					'HH_SIZE': 1 if 'null' in row['HH_SIZE'] or '+' in row['HH_SIZE'] else row['HH_SIZE'],
					'CHILDREN': 0 if 'null' in row['CHILDREN'] or '+' in row['CHILDREN'] else row['CHILDREN'],
					}

				Household.objects.create(**hargs)

			
			decoded_products = products.read().decode('utf-8').splitlines()
			reader2 = csv.DictReader(decoded_products)
			for row in reader2:
				#print(row)

				row = {k.strip():v for k, v in row.items()}

				pargs = {

					'PRODUCT_NUM' : row['PRODUCT_NUM'],
					'DEPARTMENT' : row['DEPARTMENT'],
					'COMMODITY' : row['COMMODITY'],
					'BRAND_TY' : row['BRAND_TY'],
					'NATURAL_ORGANIC_FLAG' : row['NATURAL_ORGANIC_FLAG'],
					}
				Product.objects.create(**pargs)

			decoded_transactions = transactions.read().decode('utf-8').splitlines()
			reader3 = csv.DictReader(decoded_transactions)
			for row in reader3:
				#print(len(row['BASKET_NUM']))

				row = {k.strip():v.strip() for k, v in row.items()}
				#print(row)


				targs = {

					'BASKET_NUM' : row['BASKET_NUM'],
					'HSHD_NUM' : Household.objects.get(HSHD_NUM=row['HSHD_NUM']),
					'PURCHASE' : row['PURCHASE_'],
					'PRODUCT_NUM' : Product.objects.get(PRODUCT_NUM=row['PRODUCT_NUM']),
					'SPEND' : row['SPEND'],
					'UNITS' : row['UNITS'],
					'STORE_R' : row['STORE_R'],
					'WEEK_NUM' : row['WEEK_NUM'],
					'YEAR' : row['YEAR'],
					}
				Transaction.objects.create(**targs)
			
			messages.success(request, 'Sucessfully Uploaded the datasets')
		return redirect('getHshdNum')


	tObj = Transaction.objects.filter(HSHD_NUM = 10).order_by('BASKET_NUM')
	pObj = Product.objects.filter(PRODUCT_NUM__in=[obj.PRODUCT_NUM.PRODUCT_NUM for obj in tObj]).order_by('DEPARTMENT', 'COMMODITY')

	result = {}
	i, k, r = 0, 0, 0
	length = len(pObj)
	while(length > 0):
		res = []
		res.append(str(tObj[i].HSHD_NUM))
		res.append(tObj[i].BASKET_NUM)
		res.append(tObj[i].PURCHASE)
		res.append(pObj[k].PRODUCT_NUM)
		res.append(pObj[k].COMMODITY)
		res.append(pObj[k].DEPARTMENT)
		i+=1
		k+=1
		result[r] = res
		r+=1
		length -= 1

	household = Household.objects.all()
	size= [household.HH_SIZE for household in household]
	income= [household.INCOME_RANGE for household in household]

	#print(size)
	sizeData = {}
	for d in size:
		if d not in sizeData:
			sizeData[d] = 0
		else: sizeData[d]+=1

	#print(income)
	incomeData = {}
	for data in income:
		if not 'null' in income:
			d = data.strip()
			if d not in incomeData:
				incomeData[d] = 0
			else: incomeData[d]+=1
	incomeLabel = []
	incomeCount = []
	for k, v in incomeData.items():
		if 'null' in k:
			incomeLabel.append('Under 10k')
		else:
			incomeLabel.append(k)
		incomeCount.append(v)

	print(incomeLabel, incomeCount)


	return render(request, 'assignment1/home.html', {'allUsers':allUsers, 'result': result, 'Hshd_num':10, 'incomeLabel':incomeLabel, 'incomeCount':incomeCount})

def getHshdNum(request):
	
	Hshd_num = request.POST.get('Hshd_num')

	if request.method == 'POST':

		tObj = Transaction.objects.filter(HSHD_NUM = Hshd_num).order_by('BASKET_NUM')

		#pObj = Product.objects.filter(PRODUCT_NUM__in = [obj.PRODUCT_NUM for obj in tObj]).values_list('PRODUCT_NUM', flat=True)
		#pObj = Product.objects.filter(PRODUCT_NUM__in=[obj.PRODUCT_NUM for obj in tObj]).values_list('PRODUCT_NUM', flat=True)
		pObj = Product.objects.filter(PRODUCT_NUM__in=[obj.PRODUCT_NUM.PRODUCT_NUM for obj in tObj]).order_by('DEPARTMENT', 'COMMODITY')

		#print(tObj, pObj)

		result = {}
		i, k, r = 0, 0, 0
		length = len(pObj)
		while(length > 0):
			res = []
			res.append(str(tObj[i].HSHD_NUM))
			res.append(tObj[i].BASKET_NUM)
			res.append(tObj[i].PURCHASE)
			res.append(pObj[k].PRODUCT_NUM)
			res.append(pObj[k].COMMODITY)
			res.append(pObj[k].DEPARTMENT)
			i+=1
			k+=1
			result[r] = res
			r+=1
			length -= 1

		#print(result)
		context = {'tObj':tObj}

		household = Household.objects.all()
		size= [household.HH_SIZE for household in household]
		income= [household.INCOME_RANGE for household in household]

		#print(size)
		sizeData = {}
		for d in size:
			if d not in sizeData:
				sizeData[d] = 0
			else: sizeData[d]+=1


		#print(income)
		incomeData = {}
		for data in income:
			if not 'null' in income:
				d = data.strip()
				if d not in incomeData:
					incomeData[d] = 0
				else: incomeData[d]+=1

		incomeLabel = []
		incomeCount = []
		for k, v in incomeData.items():
			if 'null' in k:
				incomeLabel.append('Under 10k')
			else:
				incomeLabel.append(k)
			incomeCount.append(v)

		print(incomeLabel, incomeCount)

		return render(request, 'assignment1/getHshdNum.html', {'result': result, 'Hshd_num':Hshd_num, 'incomeLabel':incomeLabel, 'incomeCount':incomeCount})

	

	return render(request, 'assignment1/getHshdNum.html')




def about(request):
	return render(request, 'assignment1/about.html')

def aboutContent(request):
	return render(request, 'assignment1/aboutContent.html')

def education(request):
	return render(request, 'assignment1/education.html')

def workExp(request):
	return render(request, 'assignment1/workExp.html')

def skills(request):
	return render(request, 'assignment1/skills.html')

def achievements(request):
	return render(request, 'assignment1/achievements.html')

def wordCount(filePath):
	count = 0
	with open(filePath, 'r') as f:
		for line in f.readlines():
			#print(type(str(line))
			line = str(line)
			wordCount = line.split(' ')
			count+=len(wordCount)

	return count

def downloadF(request):

	if request.user.id:

		media_root = settings.MEDIA_ROOT
		folder_path = os.path.join(media_root, request.user.username)
		for filename in os.listdir(folder_path):
			filePath = os.path.join(folder_path, filename)

		with open(filePath, 'rb') as fh:
			mime_type, _ = mimetypes.guess_type(filePath)
			response = HttpResponse(fh.read(), content_type=mime_type)
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filePath)
			return response

def register(request):

	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = UserRegisterForm()

	return render(request, 'assignment1/registration.html', {'form':form})

def profile(request):
	return render(request, 'assignment1/profile.html')

