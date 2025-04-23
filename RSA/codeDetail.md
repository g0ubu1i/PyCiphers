# 代码细节
## is_prime 函数
在代码测试时简单的写了一个判断数字是否为质数的函数
```python
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True
```
但是在实际计算时发现，由于p q过于大，导致在判断是否质数时非常缓慢。
于是在借鉴Crypto库之后，可以先用小质数表将小素数因子筛去，再做Miller-Rabin 素性测试。
这样就可以快速实现素数检测。