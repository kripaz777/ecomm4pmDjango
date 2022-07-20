from django.shortcuts import render,redirect
from .models import *
from django.views.generic import View
import datetime


# Create your views here.

class Base(View):
	views = {}
	views['categories'] = Category.objects.all()
	views['brands'] = Brand.objects.all()
	all_brand = []
	for i in Brand.objects.all():
		ids = Brand.objects.get(name = i).id
		
		count = Product.objects.filter(brand =ids).count()
		
		all_brand.append({'product_count':count,'ids' : ids})
		
	views['counts'] = all_brand
		

class HomeView(Base):
	def get(self,request):
		self.views
		self.views['sliders'] = Slider.objects.all()
		self.views['ads'] = Ad.objects.all()
		self.views['hots'] = Product.objects.filter(labels = 'hot')
		self.views['sale'] = Product.objects.filter(labels = 'sale')
		self.views['news'] = Product.objects.filter(labels = 'new')
		return render(request,'index.html',self.views)


class ProductDetailView(Base):
	def get(self,request,slug):
		self.views
		self.views['details'] = Product.objects.filter(slug = slug)
		self.views['reviews'] = Review.objects.filter(slug = slug)
		subcat = Product.objects.get(slug = slug).subcategory
		
		self.views['subcat_products'] = Product.objects.filter(subcategory = subcat)

		return render(request,'product-detail.html',self.views)

def review(request):
	if request.method == 'POST':
		# name = request.POST['name']
		# email = request.POST['email']
		name = request.user.username
		email = request.user.email
		review = request.POST['review']
		slug = request.POST['slug']
		x = datetime.datetime.now()
		date = x.strftime("%c")
		data = Review.objects.create(
			name = name,
			email = email,
			review =review,
			date = date,
			slug = slug
			)
		data.save()

	return redirect(f'/details/{slug}')


class CategoryView(Base):
	def get(self,request,slug):
		self.views
		cat_id = Category.objects.get(slug = slug).id
		self.views['cat_product'] = Product.objects.filter(category_id = cat_id)
		return render(request,'product-list.html',self.views)

class SearchView(Base):
	def get(self,request):
		self.views
		if request.method == 'GET':
			query = request.GET['query']
			self.views['search_product'] = Product.objects.filter(name__icontains = query)
			self.views['search_for'] = query
		return render(request,'search.html',self.views)

from django.contrib.auth.models import User
from django.contrib  import messages,auth
def signup(request):
	if request.method == 'POST':
		f_name = request.POST['first_name']
		l_name = request.POST['last_name']
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		cpassword = request.POST['cpassword']
		if password == cpassword:
			if User.objects.filter(username =username).exists():
				messages.error(request,'The username is already taken')
				return redirect('/signup')

			elif  User.objects.filter(email =email).exists():
				messages.error(request,'The email is already taken')
				return redirect('/signup')
			else:
				data = User.objects.create_user(
					username = username,
					email = email,
					password = password,
					first_name = f_name,
					last_name = l_name
					)
				data.save()
				return redirect('/')
		else:
			messages.error(request,'password does not match')
			return redirect('/signup')

	return render(request,'signup.html')

from django.contrib.auth import login,logout
def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username = username,password=password)
		if user is not None:
			auth.login(request,user)
			return redirect('/')

		else:
			messages.error(request,'The username or password does not match.')
			return redirect('/login')

	return render(request,'login.html')

def logout(request):
	auth.logout(request)
	return redirect('/')

def cal(slug):
	price = Product.objects.get(slug = slug).price
	discounted_price = Product.objects.get(slug = slug).discounted_price
	if discounted_price >0 :
		actual_price = discounted_price
	else:
		actual_price = price
	try:
		quantity = Cart.objects.get(slug = slug).quantity
	except:
		return actual_price


	return quantity,actual_price

def add_to_cart(request,slug):
	username = request.user.username
	if Cart.objects.filter(slug = slug,username = username,checkout = False).exists():
		quantity,actual_price = cal(slug)
		quantity = quantity+1
		total = actual_price*quantity

		Cart.objects.filter(slug = slug,username = username,checkout = False).update(
			quantity = quantity,
			total = total
			)
	else:
		actual_price= cal(slug)
		data = Cart.objects.create(
			username = username,
			slug = slug,
			total= actual_price,
			items = Product.objects.filter(slug = slug)[0]
			)
		data.save()
	return redirect('/')

