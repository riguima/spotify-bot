import string
from random import choices, randint


def generate_email() -> str:
    email = choices(string.ascii_lowercase, k=randint(8, 15))
    return ''.join(email) + '@gmail.com'


def generate_password() -> str:
    password = choices(string.printable, k=15)
    return ''.join(password)
