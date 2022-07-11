# **[set 5 - challenge 37](https://cryptopals.com/sets/5/challenges/37): Break SRP with a zero key**


## Math
Ta có
- $A = g^{a} \mod N$
- $S = g^{ab} \times g^{xub} = A^{b} \times g^{xub} \mod N$

=> Nếu A = 0 hoặc A là bội của N thì $S = 0$.

Có S, tính được key, và thêm salt từ server gửi về, sẽ tính được hmac mà không cần biết password
## Simulation
[python code](./challenge37.py)

# References