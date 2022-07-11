# **[set 5 - challenge 39](https://cryptopals.com/sets/5/challenges/39): Implement RSA**

## RSA
[RSA (Rivest–Shamir–Adleman)](https://en.wikipedia.org/wiki/RSA_(cryptosystem)): là một public-key cryptosystem.

Trong đó: encryption key được public và khác biệt với decryption key (private). Hai key được tạo ra dựa trên 2 số nguyên tố.

Sức mạnh của RSA dựa vào độ khó của `phân tích thừa số nguyên tố` hay là `factoring`.

Một video rất dễ hiểu về các công thức toán trong rsa của Khanacademy: [link](https://www.youtube.com/watch?v=wXB-V_Keiu8)

## Implement
Trong python 3.8+, hàm invmod đã có trong hàm pow:
```
from Crypto.Util.number import getPrime

# Generate 2 random primes. (1024 bit) 
p = getPrime(1024)
q = getPrime(1024)

# Your RSA math is modulo n
n = p * q

# You need this value only for keygen. 
phi = (p - 1) * (q - 1)

# Let e be 3. 
e = 3

# Compute d = invmod(e, phi).
d = pow(e, -1, phi)

# encrypt & decrypt
s = b"secret message"
encrypted = pow(int.from_bytes(s, byteorder='big'), e, n)
decrypted = pow(encrypted, d, n)
print(decrypted.to_bytes(14, byteorder='big'))
```

# References
- RSA:
    - Wikipedia: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
    - Computerphile: https://www.youtube.com/watch?v=JD72Ry60eP4
    - Khanacademy: https://www.youtube.com/watch?v=wXB-V_Keiu8