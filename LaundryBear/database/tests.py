from django.test import TestCase

from django.utils import timezone
from datetime import timedelta
from database.models import LaundryShop, Rating, Transaction, default_date

# Create your tests here.
class ModelTestCase(TestCase):
    def test_simple_location_property(self):
        shop = LaundryShop.objects.create(name='ls1', province='province1',
            barangay='barangay1', contact_number='12345',
            hours_open='24 hours', days_open='mon - sat')
        expected = 'barangay1, province1'
        self.assertEquals(shop.location, expected)

    def test_complete_location_property(self):
        shop = LaundryShop.objects.create(name='ls1', province='province1',
                city='city1', barangay='barangay1', street='street1',
                building='building1', contact_number='12345612',
                hours_open='12hours', days_open='never')
        expected = 'building1, street1, barangay1, city1, province1'
        self.assertEquals(shop.location, expected)

    def test_average_rating(self):
        shop = LaundryShop.objects.create(name='ls1', province='province1',
            barangay='barangay1', contact_number='12345',
            hours_open='24 hours', days_open='mon - sat')
        Rating.objects.create(laundry_shop=shop, paws=4)
        Rating.objects.create(laundry_shop=shop, paws=5)
        expected = (4 + 5) / 2.0
        self.assertEquals(shop.average_rating, expected)

    def test_average_rating_no_rating(self):
        shop = LaundryShop.objects.create(name='ls1', province='province1',
            barangay='barangay1', contact_number='12345',
            hours_open='24 hours', days_open='mon - sat')
        expected = 0
        self.assertEquals(shop.average_rating, expected)

    def test_default_date(self):
        date_today = timezone.now().date()
        actual = default_date().date()
        expected = date_today + timedelta(days=3)
        self.assertEquals(actual, expected)
