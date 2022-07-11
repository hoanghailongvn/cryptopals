# **[set 5 - challenge 37](https://cryptopals.com/sets/5/challenges/37): Break SRP with a zero key**


## Script
- [A] ----(p, g)----> [Eve] ----(p, 1)----> [B]:
    - [B]: $`B = g^b \mod p = 1^b \mod p = 1`$
- [B] ----(B)----> [Eve] ----(B)----> [A]: Lúc này, B đã là 1:
    - [A]: $`s = B^a \mod p = 1^a \mod p = 1`$


Ta có
- $`A = g^{a} \mod N`$
- $`S = g^{ab} \times g^{xub} = A^{b} \times g^{xub} \mod N`$

=> Nếu A = 0 hoặc A là bội của N thì $S = 0$.

Có S, tính được key, và thêm salt từ server gửi về, sẽ tính được hmac mà không cần biết password
## Simulation
[python code](./challenge37.py)

# References
