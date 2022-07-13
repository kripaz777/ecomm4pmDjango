from django.shortcuts import render,redirect
from .models import *
from django.views.generic import View
import datetime


# Create your views here.

class Base(View):
	views = {}

class HomeView(Base):
	def get(self,request):
		self.views['categories'] = Category.objects.all()
		self.views['sliders'] = Slider.objects.all()
		self.views['ads'] = Ad.objects.all()
		self.views['brands'] = Brand.objects.all()
		self.views['hots'] = Product.objects.filter(labels = 'hot')
		self.views['sale'] = Product.objects.filter(labels = 'sale')
		self.views['news'] = Product.objects.filter(labels = 'new')
		return render(request,'index.html',self.views)


class ProductDetailView(Base):
	def get(self,request,slug):
		self.views['details'] = Product.objects.filter(slug = slug)

		return render(request,'product-detail.html',self.views)

def review(request,slug):
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		review = request.POST['review']
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