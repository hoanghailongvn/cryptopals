# **[set 5 - challenge 38](https://cryptopals.com/sets/5/challenges/38): Offline dictionary attack on simplified SRP**


## simplified SRP
Là một dạng đơn giản hơn của SRP, trong public key B không còn phụ thuộc vào password nữa.

## Math
Một số công thức toán có trong simplified SRP:
- $x = hash(salt|P)$
- $u = random(0, 2^{128})$
- $v = g^{x} \mod N$
- $A = g^{a} \mod N$
- $B = g^{b} \mod N$
- $S = g^{ab + xub} \mod N$
- $K = sha256(S)$

## Dictionary attack
Vào vai một MiTM attacker, đóng giả server, gửi B, u, salt tới client để lấy được hmac value tương ứng. Dựa vào đó và bruteforce.

Chỉ có simplified SRP, MiTM attacker mới có thể bruteforce, do dựa vào b, B, u, salt và A của client, có thể tự tính được hmac tương ứng với một password nào đó:
$$ s = A^{b}\times g^{uxb} \mod N$$

Trong khi đó, với SRP, B phụ thuộc vào password nên không bruteforce được (trong công thức tính s ngoài server, cần biết a):
$$(B - k * g ^{x})^{a + u*x} \mod N $$

## Code
Tải file 10k-most-common.txt: https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt

Viết lại protocol RSP, mitm_simulate:

[python code](./challenge38.py)

Kết quả:
```
expected password: stripper
Found password: stripper
```
# References