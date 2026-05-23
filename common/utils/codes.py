import random
import string

def generate_numeric_code(length=6):
    return ''.join(random.choices(string.digits,k=length))

def generate_random_string(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits,k=length))
