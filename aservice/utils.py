import random
from django.core.cache import cache


def generate_random_code(user):
    reset_code = str(random.randint(1000000, 9999999))
    cache_key = f"password_reset_code_{user.id}"
    cache_timeout = 3600
    cache.set(cache_key, reset_code, timeout=cache_timeout)
    return reset_code


def verify_reset_code(user, code):
    cache_key = f"password_reset_code_{user.id}"
    stored_code = cache.get(cache_key)
    if stored_code and stored_code == code:
        cache.delete(cache_key)
        return True
    return False



