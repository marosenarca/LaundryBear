import time

from django.core.urlresolvers import reverse
from django.test import TestCase

from database.models import LaundryShop

# Create your tests here.
class ContextDataTestCase(TestCase):
    def test_laundry_menu_get_recent_shops(self):
        # testing only 3 visible laundry shops
        LaundryShop.objects.create(name='laundryshop1', province='lsprovince',
            barangay='lsbarangay', contact_number='123',
            hours_open='24 hours', days_open='Sun - Sat')
        time.sleep(0.1)
        LaundryShop.objects.create(name='laundryshop2', province='lsprovince',
            barangay='lsbarangay', contact_number='123',
            hours_open='24 hours', days_open='Sun - Sat')
        time.sleep(0.1)
        LaundryShop.objects.create(name='laundryshop3', province='lsprovince',
            barangay='lsbarangay', contact_number='123',
            hours_open='24 hours', days_open='Sun - Sat')
        time.sleep(0.1)
        LaundryShop.objects.create(name='laundryshop4', province='lsprovince',
            barangay='lsbarangay', contact_number='123',
            hours_open='24 hours', days_open='Sun - Sat')
        response = self.client.get(reverse('management:menu'))
        try:
            recent_shops = response.context['recent_shops']
        except:
            self.fail()
        if (recent_shops):
            shop_names = ['laundryshop2', 'laundryshop3', 'laundryshop4']
            recent_names = [shop.name for shop in recent_shops]
            set_expected = set(shop_names)
            set_actual = set(recent_names)
            self.assertEqual(
                len(set_expected.intersection(set_actual)), len(shop_names))
        else:
            self.fail()

    def test_get_shops_by_name(self):
        LaundryShop.objects.create(name='laundryshop1', province='lsprovince',
            barangay='lsbarangay', contact_number='123',
            hours_open='24 hours', days_open='Sun - Sat')
        LaundryShop.objects.create(name='laundryshop2', province='lsprovince',
            barangay='lsbarangay', contact_number='123',
            hours_open='24 hours', days_open='Sun - Sat')
        LaundryShop.objects.create(name='this should not appear',
            province='lsprovince', barangay='lsbarangay',
            contact_number='123', hours_open='24 hours',
            days_open='Sun - Sat')
        response = self.client.get(reverse('management:list-shops'),
            {'name': 'laundryshop'})
        expected_shop_list = LaundryShop.objects.filter(
            name__icontains='laundryshop')
        self.assertEqual(list(expected_shop_list),
            list(response.context['shop_list']))

    def test_get_shops_by_city(self):
        LaundryShop.objects.create(name='laundryshop1', province='lsprovince',
            barangay='lsbarangay', contact_number='123', city='citycebu',
            hours_open='24 hours', days_open='Sun - Sat')
        LaundryShop.objects.create(name='laundryshop2', province='lsprovince',
            barangay='lsbarangay', contact_number='123', city='citycebu',
            hours_open='24 hours', days_open='Sun - Sat')
        LaundryShop.objects.create(name='this should not appear',
            province='lsprovince', barangay='lsbarangay',
            contact_number='123', hours_open='24 hours',
            days_open='Sun - Sat')
        response = self.client.get(reverse('management:list-shops'),
            {'city': 'cebu'})
        expected_shop_list = LaundryShop.objects.filter(
            city__icontains='cebu')
        self.assertEqual(list(expected_shop_list),
            list(response.context['shop_list']))