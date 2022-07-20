from django.db import models
# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length = 200)
	icon = models.CharField(max_length = 200)
	slug = models.TextField(unique = True)

	def __str__(self):
		return self.name


class SubCategory(models.Model):
	name = models.CharField(max_length = 200)
	category = models.ForeignKey(Category,on_delete = models.CASCADE)
	icon = models.CharField(max_length = 200,blank = True)
	slug = models.TextField(unique = True)

	def __str__(self):
		return self.name


STATUS = (('active','Active'),('','Default'))
class Slider(models.Model):
	name = models.CharField(max_length = 200)
	image = models.ImageField(upload_to = 'media')
	text = models.TextField(blank = True)
	rank = models.IntegerField()
	status = models.CharField(choices = STATUS,blank = True,max_length=100)

	def __str__(self):
		return self.name

class Ad(models.Model):
	name = models.CharField(max_length = 400)
	image = models.ImageField(upload_to = 'media')
	text = models.TextField(blank = True)
	rank = models.IntegerField()

	def __str__(self):
		return self.name

class Brand(models.Model):
	name = models.CharField(max_length = 400)
	image = models.ImageField(upload_to = 'media')
	rank = models.IntegerField()

	def __str__(self):
		return self.name

LABELS = (('new','New'),('hot','Hot'),('sale','Sale'),('','default'))
STOCK = (('In Stock','In Stock'),('Out of Stock','Out of Stock'))
class Product(models.Model):
	name = models.CharField(max_length = 400)
	price = models.IntegerField()
	discounted_price = models.IntegerField(default = 0)
	category = models.ForeignKey(Category,on_delete = models.CASCADE)
	subcategory = models.ForeignKey(SubCategory,on_delete = models.CASCADE)
	brand = models.ForeignKey(Brand,on_delete = models.CASCADE,default = 1)
	image = models.ImageField(upload_to = 'media')
	description = models.TextField(blank = True)
	specification = models.TextField(blank = True)
	slug = models.TextField(unique = True)
	labels = models.CharField(choices = LABELS,max_length = 100)
	stock = models.CharField(choices = STOCK,max_length = 100)

	def __str__(self):
		return self.name


class Review(models.Model):
	name = models.CharField(max_length = 400)
	email = models.EmailField(max_length = 400)
	review = models.TextField(blank = True)
	date = models.CharField(max_length=200)
	slug = models.TextField()
	point = models.IntegerField(default = 1)


	def __str__(self):
		return self.name

