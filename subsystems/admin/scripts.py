import string
import random


def random_str(size=8, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))