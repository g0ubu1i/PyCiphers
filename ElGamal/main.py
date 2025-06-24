import random
from sympy.ntheory import primitive_root


def str_to_int(msg: str) -> int:
    return int.from_bytes(msg.encode('utf-8'), byteorder='big')


def int_to_str(m: int) -> str:
    byte_length = (m.bit_length() + 7) // 8
    return m.to_bytes(byte_length, byteorder='big').decode('utf-8')


_SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
    101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
    151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
    211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271,
    277, 281, 283, 293
]


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

    return True


def generate_prime(bits=512):
    while True:
        prime = random.getrandbits(bits)
        if is_prime(prime):
            return prime


class ElGamal:
    def __init__(self):
        self.p = generate_prime(256)
        self.g = primitive_root(self.p)
        self.k = random.randint(2, self.p - 2)
        self.y = pow(self.g, self.k, self.p)

    def encrypt(self, msg):
        m = str_to_int(msg)
        r = random.randint(2, self.p - 2)
        y1 = pow(self.g, r, self.p)
        y2 = (m * pow(self.y, r, self.p)) % self.p
        return y1, y2

    def decrypt(self, cipher):
        y1, y2 = cipher
        m = (y2 * pow(y1, self.p - self.k - 1, self.p)) % self.p
        return int_to_str(m)


ElGamal = ElGamal()
print(ElGamal.encrypt("Hello World!"))
print(ElGamal.decrypt(ElGamal.encrypt("Hello World!")))
