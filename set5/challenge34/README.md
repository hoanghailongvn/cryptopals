# **[set 5 - challenge 34](https://cryptopals.com/sets/5/challenges/34): Implement a MITM key-fixing attack on Diffie-Hellman with parameter injection**

MITM là một cách tấn công, trong đỏ, kẻ tấn công đứng ở giữa kết nối giữa 2 bên, có thể đọc và chỉnh sửa message giữa 2 bên.

Trong challenge này, kẻ tấn công là M đứng ở giữa 2 người A và B, chỉnh sửa `g` và `B` trong qua trình Diffie-Hellman key exchange, khiến:
- [B]: s = (g^b) % p = (p^b) % p = 0
- [A]: s = (B^a) % p = (p^a) % p = 0

Khi này attacker đã làm cho s cả hai bên đều bằng 0 => đã biết private key, có thể đọc được tin nhắn đã mã hóa giữa 2 bên

## Code
[here](./challenge34.py)

Kết quả:
```
A send: p g A: (37, 5, 2)
B received p g a: (37, 5, 37)
B s: 0
B key: b'\xb3v\x88Z\xc8E+l\xbf\x9c\xed\x81\xb1\x08\x0b\xfd'
B send "B": 36
A recv "B": 37
A s: 0
A key: b'\xb3v\x88Z\xc8E+l\xbf\x9c\xed\x81\xb1\x08\x0b\xfd'
A send: b'private message'
mitm: b'private message'
```
# References
