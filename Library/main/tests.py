from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory
from testbase import create_random_user, write_percentage, count_delta

from book_library.views import *


class AvailabilityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = create_random_user()
        self.admin = create_random_user()
        self.admin[0].is_staff = True
        self.admin[0].save()
        self.urls_to_test = ['mainpage', 'openid-login']

    def test_availability(self):
        delta_percent = count_delta(len(self.urls_to_test))
        percentage = float(0)
        for url in self.urls_to_test:
            percentage = write_percentage(percentage, delta_percent)
            urln = url
            request = self.client.get(reverse(urln))
            self.assertTrue(request.status_code != 404)
