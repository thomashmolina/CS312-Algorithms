import random


def prime_test(N: int, k: int) -> tuple:
    # This is main function, that is connected to the Test button. You don't need to touch it.
    return fermat(N, k), miller_rabin(N, k)


def mod_exp(x: int, y: int, N: int) -> int:
    result = 1
    x = x % N
    while y > 0:
        if y & 1 == 1:
            result = (result * x) % N
        y = y >> 1
        x = (x * x) % N
    return result


def fprobability(k: int) -> int:
    # You will need to implement this function and change the return value.
    return 1 - (2 ** -k)


def mprobability(k: int) -> float:
    # You will need to implement this function and change the return value.
    return 1 - (4 ** -k)


# finds the greatest common denominator
def gcd(a: int, b: int) -> int:  # O(log n)
    if b == 0:
        raise ValueError("Cannot modulus by 0")
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


def fermat(N: int, k: int) -> str:
    if N == 2:  # O(1)
        return 'prime'
    # 0, 1, and even numbers are composite
    if not N & 1 or N <= 1:  # O(1)
        return 'composite'
    # 2, 3 are prime
    if N <= 3:  # O(1)
        return 'prime'

    while k > 0:  # O(1)
        a = random.randint(2, N - 2)  # O(log n)
        if gcd(N, a) != 1:  # if greatest common denominator != 1 return composite
            return 'composite'

        if mod_exp(a, N - 1, N) != 1:  # if a raised to the N-1 power modulus N is != 1 it is composite
            return 'composite'
        k -= 1
    return 'prime'


# general methodology for finding a prime
def isPrime(N: int, k: int) -> str:
    if N == 2:  # 2 is prime
        return 'prime'
    if N <= 1 or not N & 1:  # 0, 1, even numbers
        return 'composite'
    if N <= 3:  # 2, 3 are prime
        return 'prime'
    d = N - 1
    while d % 2 == 0:  # O(log n)
        d /= 2
    for i in range(k):  # O(log n)
        if miller_rabin(N, d) == 'composite':
            return 'composite'
    return 'prime'


def miller_rabin(N: int, k: int) -> str:
    if N == 2:  # O(1)
        return 'prime'
    if N <= 1 or not N & 1:  # O(1)
        return 'composite'
    if N <= 3:  # O(1)
        return 'prime'

    d = N - 1
    while d % 2 == 0:  # O(1)
        d /= 2
    d = int(d)

    iterations = k
    for i in range(iterations):  # O(log n)
        a = random.randint(2, N - 2)
        x = mod_exp(a, d, N)
        if x == 1 or x == N - 1:
            break
        while d != N - 1:
            x = mod_exp(x, 2, N)
            d *= 2
            if x == 1:
                return 'composite'
            if x == N - 1:
                break
    return 'prime'


def mod_exp_test():
    x, y, N = (2, 3, 5)
    result = mod_exp(x, y, N)
    if result != 3:
        raise ValueError(f"result not 3, result: {result}")
    x, y, N = (2, 5, 13)
    result = mod_exp(x, y, N)
    if result != 6:
        raise ValueError(f"result not 3, result: {result}")


def test():
    with open('primes.txt', 'r') as readfile:
        lines = readfile.read().split(" ")
        prime_numbers = []
        for l in lines:
            if l != '':
                try:
                    prime_numbers.append(int(l))
                except Exception as e:
                    pass
        print(prime_numbers)
    for item in prime_numbers:
        p = prime_test(item, 10)
        if p == ('prime', 'prime'):
            print(f'test failed at {item}')
            raise Exception('test failed')


if __name__ == "__main__":
    print(mod_exp(2, 125, 7))
