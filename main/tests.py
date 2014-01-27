from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from Library.testbase import create_random_user, write_percentage, count_delta


class AvailabilityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = create_random_user()
        self.admin = create_random_user()
        self.admin[0].is_staff = True
        self.admin[0].save()
        self.urls_to_test = ['mainpage', 'openid-login', 'openid-complete', 'landing_page', 'thanks', 'auth_login']

    def test_availability(self):
        delta_percent = count_delta(len(self.urls_to_test))
        percentage = float(0)
        for url in self.urls_to_test:
            percentage = write_percentage(percentage, delta_percent)
            urln = url
            request = self.client.get(reverse(urln))
            self.assertTrue(request.status_code != 404)

    def test_login_post_request(self):
        request = self.client.post(reverse('auth_login'),
                                   {'username': self.user[0].username, 'password': self.user[1]})
        self.assertEqual(request.status_code, 302)

    def test_landing_page_post_request(self):
        request = self.client.post(reverse('landing_page'), {'email': self.user[0].email})
        self.assertEqual(request.status_code, 302)