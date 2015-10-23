from django.db import models

# Create your models here.
class LaundryShop(models.Model):
	name = models.CharField(max_length=50, blank=False)
	province = models.CharField(max_length=50, blank=False)
	city = models.CharField(max_length=50, blank=True)
	barangay = models.CharField(max_length=50, blank=False)
	street = models.CharField(max_length=50, blank=True)
	building = models.CharField(max_length=50, blank=True)
	contact_number = models.CharField(max_length=30, blank=False)
	email = models.EmailField(blank=True)
	website = models.URLField(blank=True)
	hours_open = models.CharField(max_length=100, blank=False)
	days_open = models.CharField(max_length=100, blank=False)
	

class Service(models.Model):
	name = models.CharField(max_length=100, blank=False)
	description = models.TextField(blank=False)
	prices = models.ManyToManyField('LaundryShop', through='Price',
		related_name='services')

class Price(models.Model):
	laundry_shop = models.ForeignKey('LaundryShop', on_delete=models.CASCADE)
	service = models.ForeignKey('Service', on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)

class Rating(models.Model):
	laundry_shop = models.ForeignKey('LaundryShop', related_name='ratings')
	paws = models.IntegerField(null=True, blank=True)