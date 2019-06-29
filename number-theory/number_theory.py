from random import randint
from math import sqrt


def gcd(a, b):
    """
    euclidean algorithm
    :return: the gcd of a and b
    """
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def ext_euclid(a, b):
    """
    extended euclidean algorithm
    :return: (g, x, y) s.t. x*a + y*b  = gcd(a, b)
    """
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = ext_euclid(b, a % b)
        return d, y, x - a // b * y


def inv(x, n):
    """
    :return: the inverse of x mod n
    """
    assert gcd(x, n) == 1, "the inverse doesn't exist"
    # ax + bn = 1 gives a = x^-1 mod n
    return ext_euclid(x, n)[1]


def linear_congruence(a, b, n):
    """
    solve linear congruence ax = b mod n
    :return: x mod n
    """
    assert b % gcd(a, n) == 0, "the congruence doesn't have solutions"

    d = gcd(a, n)

    # the congruence has a unique solution in Zn
    if d == 1:
        return (b * inv(a, n)) % n

    # the congruence has d solutions in Zn
    if d > 1 and b % d == 0:
        a //= d
        b //= d
        n //= d
        x = (b * inv(a, n)) % n

        sols = []
        for _ in range(d):
            sols.append(x)
            x += n
        return sols


def crt(b, n):
    """
    chinese remainder theorem
    solve x = b[i] mod n[i] for i=1..r
    :return: the unique simultaneous solution mod p = n1n2...nr
    pre-condition: n[i] pairwise co-prime for i=1..r
    """
    r = len(b)

    p = 1
    for i in range(r):
        p *= n[i]

    m = [p // n[i] for i in range(r)]

    v = [inv(m[i], n[i]) for i in range(r)]

    # for each b[i] * m[i] * v[i]:
    # m[i] v[i] are inverses, after mod p only b[i] left
    # all the other terms since m[i] contain n[i], mod p gives 0
    return sum([b[i] * m[i] * v[i] for i in range(r)]) % p


def fast_exponentiation(a, b, n):
    """
    :return: a^b mod n
    """
    # write b in binary
    bits = "{0:b}".format(b)
    d = 1
    for bit in bits:
        d = d ** 2 % n
        if bit == '1':
            d = d * a % n
    return d


def is_prime(n):
    """
    miller rabin primality test
    :return: True if n is PROBABLY prime, False if n is composite
    """
    # the probability of wrong conclusion is not more than (1/4)^s
    s = 50
    for _ in range(s):
        a = randint(2, n - 1)
        # use fast exponentiation to compute a^(n-1) mod n
        bits = "{0:b}".format(n - 1)
        d = 1
        for bit in bits:
            prev_d = d
            d = d ** 2 % n
            # if n is prime then 1, n-1 are the only solutions to x^2=1 mod n
            if d == 1 and prev_d != 1 and prev_d != n - 1:
                return False
            if bit == '1':
                d = d * a % n
        # if n is prime then a^(n-1) = 1 mod n (fermat's little theorem)
        if d != 1:
            return False
    return True


def pollard_rho(n):
    """
    :return: a non-trivial factor of a composite number n
    """
    x = randint(0, n - 1)  # x1: a random element in Zn
    y = x  # y stores x1, x2, x4, x8, x16, ...
    k = 2  # k facilitates y
    for i in range(2, int(sqrt(n))):
        x = (x ** 2 - 1) % n
        d = gcd(y - x, n)
        if d != 1 and d != n:
            return d
        if i == k:
            y = x
            k *= 2
    # after certain iterations (sqrt(n)), if we still couldn't find a factor,
    # then we have to try a different value of x1
    return pollard_rho(n)


def main():
    assert ext_euclid(1914, 899) == (29, 8, -17)
    assert linear_congruence(12, 15, 21) == [3, 10, 17]
    assert crt([5, 4, 3], [6, 11, 17]) == 785
    assert fast_exponentiation(3, 99, 100) == 67
    primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
              107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]
    for x in range(3, 200):
        if x in primes:
            assert is_prime(x)
        else:
            assert not is_prime(x)


if __name__ == '__main__':
    main()
