import random
from Crypto.Util.number import *


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 % m0


_SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
    101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
    151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
    211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271,
    277, 281, 283, 293
]


# 判断一个大数是否为素数（类似 Crypto.Util.number.isPrime）
def is_prime(n, rounds=16):
    if n < 2:
        return False
    for p in _SMALL_PRIMES:
        if n % p == 0:
            return n == p  # 若 n 是小素数之一返回 True

    # 分解 n-1 为 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # Miller-Rabin 测试
    for _ in range(rounds):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue  # 可能是素数

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # 合数

    return True  # 极大概率是素数


def generate_prime(bits=512):
    while True:
        prime = random.getrandbits(bits)
        if is_prime(prime):
            return prime


def generate_keys():
    p = generate_prime()
    q = generate_prime()
    while q == p:
        q = generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = generate_prime(25)
    while gcd(e, phi) != 1:
        e = generate_prime(25)
    # 计算 d（私钥）
    d = mod_inverse(e, phi)
    return (e, n), (d, n)


def str_to_int(msg: str) -> int:
    return int.from_bytes(msg.encode('utf-8'), byteorder='big')


def int_to_str(m: int) -> str:
    byte_length = (m.bit_length() + 7) // 8
    return m.to_bytes(byte_length, byteorder='big').decode('utf-8')


def encrypt(msg, public_key):
    e, n = public_key
    return pow(str_to_int(msg), e, n)


def decrypt(c, private_key):
    d, n = private_key
    return pow(c, d, n)


if __name__ == '__main__':
    ExampleMsg = "Hello, World!"
    public_key, private_key = generate_keys()
    c = encrypt(ExampleMsg, public_key)
    m = decrypt(c, private_key)
    print(int_to_str(m))
