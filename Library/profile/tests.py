from types import TupleType
import random

from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory

from testbase import create_random_user, write_percentage, count_delta
from book_library.views import *

MAX_NUMBER_OF_ADMINS = 6

MAX_NUMBER_OF_USERS = 25


class RestrictionsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.users = [create_random_user() for item in range(1, random.randint(1, MAX_NUMBER_OF_USERS))]
        self.admins = list()
        for item in range(1, random.randint(1, MAX_NUMBER_OF_ADMINS)):
            user = create_random_user()
            user[0].is_staff = True
            user[0].save()
            self.admins.append(user)
        urls_to_test = ['profile:all',]
        for user in User.objects.all():
            urls_to_test.append((('profile:profile', user.pk)))
            urls_to_test.append((('profile:change', user.pk)))
        self.urls_to_test = urls_to_test

    def test_availability(self):
        delta_percent = count_delta(len(self.urls_to_test))
        percentage = float(0)
        for url in self.urls_to_test:
            percentage = write_percentage(percentage, delta_percent)
            if type(url) is TupleType:
                urln = url[0]
                urlp = url[1]
                request = self.client.get(reverse(urln, kwargs={'pk': urlp}))
            else:
                urln = url
                request = self.client.get(reverse(urln))
            self.assertTrue(request.status_code != 404)

    def test_logged_out_rights(self):
        delta_percent = count_delta(len(self.urls_to_test))
        percentage = float(0)
        for url in self.urls_to_test:
            percentage = write_percentage(percentage, delta_percent)
            if type(url) is TupleType:
                urln = url[0]
                urlp = url[1]
                request = self.client.get(reverse(urln, kwargs={'pk': urlp}))
            else:
                urln = url
                request = self.client.get(reverse(urln))
            self.assertTrue(request['location'].startswith('http://testserver/auth/login?next='))

    def test_user_rights(self):  # User and admin have equal rights here
        urls_to_test = [x for x in self.urls_to_test if not (type(x) is TupleType and x[0].endswith('change'))]
        restricted_urls = [x for x in self.urls_to_test if type(x) is TupleType and x[0].endswith('change')]
        delta_percent = count_delta(len(self.users + self.admins))
        percentage = float(0)
        for user in self.users + self.admins:
            percentage = write_percentage(percentage, delta_percent)
            self.client.login(username=user[0].username, password=user[1])
            for url in urls_to_test:
                if type(url) is TupleType:
                    urln = url[0]
                    urlp = url[1]
                    request = self.client.get(reverse(urln, kwargs={'pk': urlp}))
                else:
                    urln = url
                    request = self.client.get(reverse(urln))
                if request.status_code == 200:
                    self.assertEqual(request.status_code, 200)
            for url in restricted_urls:
                if type(url) is TupleType:
                    urln = url[0]
                    urlp = url[1]
                    request = self.client.get(reverse(urln, kwargs={'pk': urlp}))
                if user[0].pk == urlp:
                    self.assertEqual(request.status_code, 200)
                else:
                    self.assertEqual(request.status_code, 302)
            self.client.logout()