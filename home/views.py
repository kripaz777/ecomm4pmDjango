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
		name = request.POST['name']
		email = request.POST['email']
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