from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta


# Create your models here.
class UserProfile(models.Model):
    client = models.OneToOneField(User)
    province = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=True)
    barangay = models.CharField(max_length=50, blank=False)
    street = models.CharField(max_length=50, blank=True)
    building = models.CharField(max_length=50, blank=True)
    contact_number = models.CharField(max_length=30, blank=False)

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
        average = 0
        for shops in self.price_set.order_set.transaction_set.distinct():
            for order in shops..all():
                average += order.transaction.paws
        return average/2

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
    paws = models.IntegerField(blank=False)
    status = models.IntegerField(choices=TRANSACTION_STATUS_CHOICES, default=1)
    request_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(default=default_date)

    def __unicode__(self):
        return "{0}".format(unicode(self.request_date))
