# 密钥生成

1.选取一个大素数p

2.选取$Z^*_p$的生成元g

3.随机选取整数k,要求$0 \leqslant k \leqslant p-2 $,计算$g^k \equiv y \mod p$。

其中私钥为{k}，公钥为{p,g.y}

# 加密

Alice选择随机数$r \in Z_{p-1}$,对明文加密$E_k(m,r)= (y_1,y_2)$。

其中
$$
y_1 \equiv g^r \mod p \\

y_2 \equiv my^r \mod p
$$

# 解密

$$
D_k(y_1,y_2) = y_2(y_1^k)^{-1} \mod p \equiv m(g^k)^r(g^{rk})^{-1} \equiv m \mod p
$$







