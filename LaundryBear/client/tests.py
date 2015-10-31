from django.test import TestCase

# Create your tests here.
"""
class LoginTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='test', password='runner')

    def test_login_required_redirect(self):
        response = self.client.get(reverse('management:menu'), follow=True)
        expected = 'management/account/login.html'
        self.assertEqual(response.templates[0].name, expected)

    def test_redirect_to_menu_after_login_with_next(self):
        response = self.client.get(reverse('management:menu'), follow=True)
        request = response.request
        response = self.client.post('{0}?{1}'.format(request['PATH_INFO'],
            request['QUERY_STRING']),
            {'username': 'test', 'password': 'runner'}, secure=True,
            follow=True)
        expected = 'management/shop/laundrybearmenu.html'
        self.assertEqual(response.templates[0].name, expected)

    def test_invalid_login(self):
        response = self.client.get(reverse('management:menu'), follow=True)
        request = response.request
        response = self.client.post('{0}?{1}'.format(request['PATH_INFO'],
            request['QUERY_STRING']),
            {'username': 'tester', 'password': 'runner'}, secure=True,
            follow=True)
        expected = 'management/shop/laundrybearmenu.html'
        self.assertNotEqual(response.templates[0].name, expected)

    def test_redirect_to_menu_after_login_without_next(self):
        response = self.client.post(reverse('management:login-admin'),
            {'username': 'test', 'password': 'runner'}, secure=True,
            follow=True)
        expected = 'management/shop/laundrybearmenu.html'
        self.assertEqual(response.templates[0].name, expected)
"""
