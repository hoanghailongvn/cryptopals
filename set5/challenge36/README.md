# **[set 5 - challenge 36](https://cryptopals.com/sets/5/challenges/36): Implement Secure Remote Password (SRP)**

## Secure Remote Password
[SRP (Secure Remote Password protocol)](https://en.wikipedia.org/wiki/Secure_Remote_Password_protocol): là giao thức giúp server xác thực người dùng thông qua mật khẩu.

Điểm đặc biệt là phía server không lưu giá trị của password, dù là hash. 

## Math
Một số công thức toán có trong giao thức.
- $x = hash(salt|P)$
- $u = hash(A|B)$
- $v = g^{x} \mod N$
- $A = g^{a} \mod N$
- $B = kv + g^{b} \mod N$
- $S = g^{ab} \times g^{xub} \mod N$

Trong đó, những nội dung public là: salt, A, B.

Trong public B có ảnh hưởng của password

## Simulation
[python code](./challenge36.py)
# References
- SRP:
    - https://www.youtube.com/watch?v=RWksEY-Bf9I
    - https://en.wikipedia.org/wiki/Secure_Remote_Password_protocol
- Salt:
    - https://en.wikipedia.org/wiki/Salt_(cryptography)