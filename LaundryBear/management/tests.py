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
        LaundryShop.objects.create(name='laundryshop2', province='lsprovince',
            barangay='lsbarangay', contact_number='123',
            hours_open='24 hours', days_open='Sun - Sat')
        LaundryShop.objects.create(name='laundryshop3', province='lsprovince',
            barangay='lsbarangay', contact_number='123',
            hours_open='24 hours', days_open='Sun - Sat')
        LaundryShop.objects.create(name='laundryshop4', province='lsprovince',
            barangay='lsbarangay', contact_number='123',
            hours_open='24 hours', days_open='Sun - Sat')
        response = self.client.get(reverse('management:menu'))
        recent_shops = response.context.get('recent_shops', False)
        if (recent_shops):
            shop_names = ['laundryshop2', 'laundryshop3', 'laundryshop4']
            recent_names = [shop.name for shop in recent_shops]
            set_expected = set(shop_names)
            set_actual = set(recent_names)
            self.assertEqual(
                len(set_expected.intersection(set_actual)), len(shop_names))
        else:
            self.fail()
