from django.contrib.auth.models import User

import string
import random
from sys import stdout


def random_string(size=6, chars=string.printable, at_least_one_char=False):
    if at_least_one_char:
        size -= 1
    random_string = [random.choice(chars) for x in range(size)]
    if at_least_one_char:
        random_string.insert(random.randint(0, size-1),
                             random.choice(string.letters))
    return ''.join(random_string)


def create_random_user():  # returns a tuple of user and his password
    users_password = random_string(random.randint(8, 100))
    return (User.objects.create_user(username=random_string(30, at_least_one_char=True),
                                email=random_string(size=random.randint(2, 50),
                                                    chars=string.letters + string.digits,
                                                    at_least_one_char=True)+"@gmail.com",
                                password=users_password,
                                first_name=random_string(size=random.randint(1, 30),
                                                         chars=string.letters),
                                last_name=random_string(size=random.randint(1, 30),
                                                        chars=string.letters)),
            users_password,)


def write_percentage(percentage, delta_percent):
    percentage += delta_percent  # 1 division and NUMBER_OF_ITERATIONS additions. It is faster than obvious method
    stdout.write("\rTest preformed: %d %%" % percentage)
    stdout.flush()
    return percentage


def count_delta(denominator):
    return float(1*100) / denominator