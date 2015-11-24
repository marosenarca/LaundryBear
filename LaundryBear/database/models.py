from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.sites.models import Site
from datetime import timedelta


# Create your models here.
class UserProfile(models.Model):
    client = models.OneToOneField(User)
    contact_number = models.CharField(max_length=30, blank=False)
    province = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=True)
    barangay = models.CharField(max_length=50, blank=False)
    street = models.CharField(max_length=50, blank=True)
    building = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.client.get_full_name()

    @property
    def location(self):
        address = [self.building, self.street, self.barangay, self.city,
            self.province]
        while '' in address:
            address.remove('')
        return ', '.join(address)

class LaundryShop(models.Model):
    class Meta:
        get_latest_by = 'creation_date'
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
    creation_date = models.DateTimeField(auto_now_add=True)

    @property
    def location(self):
    	address = [self.building, self.street, self.barangay, self.city,
    		self.province]
        while '' in address:
        	address.remove('')
        return ', '.join(address)

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if not ratings:
            return 0
        sum_ratings = 0.0
        for rating in ratings:
            sum_ratings += rating.paws
        return sum_ratings / len(ratings)

    def __unicode__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    description = models.TextField(blank=False)
    prices = models.ManyToManyField('LaundryShop', through='Price',
        related_name='services')

    def __unicode__(self):
        return self.name

class Price(models.Model):
    laundry_shop = models.ForeignKey('LaundryShop', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    duration = models.IntegerField()

class Rating(models.Model):
    laundry_shop = models.ForeignKey('LaundryShop', related_name='ratings')
    paws = models.IntegerField(blank=False)

    def __unicode__(self):
        return "{1} paw rating for {0}".format(unicode(self.laundry_shop),self.paws)

class Order (models.Model):
    price = models.ForeignKey('Price')
    transaction = models.ForeignKey('Transaction')
    pieces = models.IntegerField(default=0)

def default_date():
    return timezone.now()+timedelta(days=3)

class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'Ongoing'),
        (3, 'Done'),
        (4, 'Rejected')
    )

    def get_choice_name(self):
        return self.TRANSACTION_STATUS_CHOICES[self.status - 1][1]

    client = models.ForeignKey('UserProfile')
    status = models.IntegerField(choices=TRANSACTION_STATUS_CHOICES, default=1)
    request_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(default=default_date)
    province = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=True)
    barangay = models.CharField(max_length=50, blank=False)
    street = models.CharField(max_length=50, blank=True)
    building = models.CharField(max_length=50, blank=True)
    price = models.IntegerField(blank=False, default=0)

    @property
    def location(self):
    	address = [self.building, self.street, self.barangay, self.city,
    		self.province]
        while '' in address:
        	address.remove('')
        return ', '.join(address)

    def __unicode__(self):
        return "{0}".format(unicode(self.request_date))


class Fees(models.Model):
    delivery_fee = models.DecimalField(default=50, decimal_places=2,
        max_digits=4)
    service_charge = models.DecimalField(default=0.1, decimal_places=2,
        max_digits=3)
    site = models.OneToOneField(Site)
