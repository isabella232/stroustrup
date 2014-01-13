from types import TupleType
import random
import os
import string
from django.utils import timezone
from sys import stdout

from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory

from registration.models import RegistrationProfile

from testbase import create_random_user, write_percentage, count_delta, random_string
from Library.book_library.views import *

os.environ['RECAPTCHA_TESTING'] = 'True'  # read https://pypi.python.org/pypi/django-recaptcha

NUMBER_OF_ITERATIONS = 500  # in registration test

MAX_PASSWORD_LENGTH = 250

MAX_EMAIL_LENGTH = 100


class AvailabilityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.urls_to_test = ['auth_login', 'auth_logout', 'registration_register']

    def test_availability(self):
        delta_percent = count_delta(len(self.urls_to_test))
        percentage = delta_percent
        for url in self.urls_to_test:
            percentage = write_percentage(percentage, delta_percent)
            urln = url
            request = self.client.get(reverse(urln))
            self.assertTrue(request.status_code != 404)

    def test_registration(self):
        users_count = 0
        delta_percent = count_delta(NUMBER_OF_ITERATIONS)
        percentage = delta_percent
        for i in range(1, NUMBER_OF_ITERATIONS):
            percentage = write_percentage(percentage, delta_percent)
            username = random_string(size=(random.randint(1, 26)), chars=string.letters) + str(i)
            password = random_string(random.randint(8, MAX_PASSWORD_LENGTH))
            email = random_string(size=random.randint(2, MAX_EMAIL_LENGTH),
                                                    chars=string.letters + string.digits,
                                                    at_least_one_char=True)+"@gmail.com"
            pass_are_equal = random.randint(0, 1)
            if pass_are_equal:  # randomize passwords equality
                password2 = password
            else:
                password2 = password
                list_pass = list(password2)
                list_pass = chr(ord(password2[0]) + 1)
                password2 = ''.join(list_pass)
            request = self.client.post(reverse('registration_register'), {'username': username,
                                                                 'password1': password,
                                                                 'password2': password2,
                                                                 'email': email,
                                                                 'recaptcha_response_field': 'PASSED'})
            if pass_are_equal:
                users_count += 1
                add = 1
                self.assertEqual(302, request.status_code)
                self.assertEqual('http://testserver/accounts/register/complete/', request['location'])
                new_user = User.objects.get(pk=users_count)
                self.assertEqual(new_user.is_active, False)
                new_profile = RegistrationProfile.objects.get(pk=users_count)
                request = self.client.get("http://testserver/accounts/activate/" + new_profile.activation_key +'/')
                new_user = User.objects.get(pk=users_count)
                self.assertEqual(new_user.is_active, True)

                request = self.client.post(reverse('auth_login'), {'username': new_user.username,
                                                                  'password': password})
                new_user = User.objects.get(pk=users_count)
                self.assertEqual('http://testserver/', request['location'])
                delta = new_user.last_login - timezone.now()
                self.assertTrue(delta.total_seconds() < 1)
            else:
                self.assertTrue(not request.context_data['form'].is_valid())




