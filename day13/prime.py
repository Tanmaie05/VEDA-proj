import math

def is_prime(n):
    if n <= 1:
        return False

    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False

    return True


def generate_primes(start, end):
    prime_list = []

    for num in range(start, end + 1):
        if is_prime(num):
            prime_list.append(num)

    return prime_list