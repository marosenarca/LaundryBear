from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    client = models.OneToOneField(User)
    contact_number = models.CharField(max_length=30, blank=False)
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
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    prices = models.ManyToManyField('LaundryShop', through='Price',
        related_name='services')

    def __unicode__(self):
        return self.name


class Price(models.Model):
    laundry_shop = models.ForeignKey('LaundryShop', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)


class Rating(models.Model):
    laundry_shop = models.ForeignKey('LaundryShop', related_name='ratings')
    paws = models.IntegerField(blank=False)

    def __unicode__(self):
        return "{1} paw rating for {0}".format(unicode(self.laundry_shop),self.paws)
