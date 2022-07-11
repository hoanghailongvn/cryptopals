# **[set 5 - challenge 35](https://cryptopals.com/sets/5/challenges/35): Implement DH with negotiated groups, and break with malicious "g" parameters**

```
1: A->B
Send "p", "g"
2: B->A
Send ACK
3: A->B
Send "A"
4: B->A
Send "B"
5: A->B
Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
6: B->A
Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv
```

Tại bước 1, mitm attacker thay "g" = 1:
- [B]: $`B = g^b \mod p = 1`$
- => [A]: $`s = B^a \mod p = 1`$ 

=> attacker biết `s` phía A là 1

Nếu g = p
- [B]: $`B = g^b \mod p = 0`$
- => [A]: $`s = B^a \mod p = 0`$

=> attacker biết `s` phía A là 0

Nếu g = p - 1:

có công thức: $`((p - 1)^a) \mod p =`$
- a chẵn: 1
- a lẻ: p - 1

=> attacker cũng xác định được `s` ở phía A

## Code với g = 1
[here](./challenge35.py)

Kết quả:
```
A send: p g A: (37, 5, 28)
B received p g a: (37, 1, 28)
B s: 27
B key: b'\xf0\xbb`\x8a6\x1a\xfa\xa1SV\xa9P\xd9m\xa5\x9b'
B send B: 1
A recv: B: 1
A s: 1
A key: b'\xb0\xdf`k\x85\xdfG}\x99\x05\xd3\xd5\xeaU\x85\xfa'
A send: b'private message'
b'private message'
```
Chú ý rằng, key, g, s hai bên A và B giờ đã khác nhau.
# References
