# **[set 5 - challenge 40](https://cryptopals.com/sets/5/challenges/40): Implement an E=3 RSA Broadcast attack**

## Håstad's broadcast attack
Trong RSA, khi cùng một plaintext được mã hóa `e` lần trở lên bằng `e` public key khác nhau, plaintext có thể dễ dàng bị tìm ra bởi kẻ tấn công.



## Implement
Python code:
```
from Crypto.Util.number import getPrime

p0 = getPrime(1024)
p1 = getPrime(1024)
p2 = getPrime(1024)
q0 = getPrime(1024)
q1 = getPrime(1024)
q2 = getPrime(1024)

n0 = p0 * q0
n1 = p1 * q1
n2 = p2 * q2
e = 3

# encrypt & decrypt
s = 42
c0 = pow(s, e, n0)
c1 = pow(s, e, n1)
c2 = pow(s, e, n2)

result = (
    c0 * n1 * n2 * pow(n1 * n2, -1, n0) +
    c1 * n0 * n2 * pow(n0 * n2, -1, n1) +
    c2 * n0 * n1 * pow(n0 * n1, -1, n2)
) % (n0 * n1 * n2)

decrypted = round(pow(result, 1/3))

print(decrypted)
```

# References
- Håstad's broadcast attack:
    - Wikipedia: https://en.wikipedia.org/wiki/Coppersmith's_attack#H%C3%A5stad's_broadcast_attack
