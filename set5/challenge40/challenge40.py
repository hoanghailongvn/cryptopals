from Crypto.Util import number

p1 = number.getPrime(1024)
p2 = number.getPrime(1024)
p3 = number.getPrime(1024)
q1 = number.getPrime(1024)
q2 = number.getPrime(1024)
q3 = number.getPrime(1024)

n1 = p1 * q1
n2 = p2 * q2
n3 = p3 * q3
e = 3

# encrypt & decrypt
s = 42
e1 = pow(s, e, n1)
e2 = pow(s, e, n2)
e3 = pow(s, e, n3)

result = (
    e1 * n2 * n3 * pow(n2 * n3, -1, n1) +
    e2 * n1 * n3 * pow(n1 * n3, -1, n2) +
    e3 * n1 * n2 * pow(n1 * n2, -1, n3)
) % (n1 * n2 * n3)

decrypted = round(result ** (1/3))

assert decrypted == s