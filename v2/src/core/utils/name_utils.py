# v2/src/core/utils/random_utils.py
import random
import string


def rand_name(n: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choices(alphabet, k=n))
