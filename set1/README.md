# Writeups
- https://viblo.asia/p/cryptopals-set-1-basics-4dbZNJNkZYM
- https://cedricvanrompay.gitlab.io/cryptopals/challenges/01-to-08.html
# Python
## b''
The b" notation is used to specify a bytes string in Python.

## bytes
The `bytes` is an array of byte variables where each hexadecimal element has a value between 0 and 255.
```
a = b'abcdef'

print(a)
print(a[0])
print(type(a))
print(type(a[0]))
```
Output:
```
b'abcdef'                                                                                                                       
97                                                                                                                              
<class 'bytes'>                 
<class 'int'>
```

## from binascii import hexlify
```
hexlify: (data: ReadableBuffer, sep: str | bytes = ..., bytes_per_sep: int = ...) -> bytes
Hexadecimal representation of binary data.
```
Input là `str`, output là `bytes`
Example:
```
from binascii import hexlify

x = "Hello"
res = bytes(x, 'utf-8')

print(hexlify(res))
print(hexlify(res , '-'))
```
Output:
```
b'48656c6c6f'
b'48-65-6c-6c-6f'
```
## from binascii import unhexlify
```
def unhexlify(hex_: str) -> bytes:
    # strip 0x at the beginning if needed
    hex_ = hex_.lstrip('0x')
    # zero-padding
    if len(hex_) % 2: hex_ = '0' + hex_
    bytelist = []
    for i in range(0, len(hex_), 2):
        bytelist.append(int(hex_[i * 2 : i * 2 + 2], 16))
    return bytes(bytelist)
```
Example:
```
from binascii import hexlify, unhexlify

res = b"Hello"
w = hexlify(res)

print(f"unhexlify({w}) => {unhexlify(w)}")
```
Output:
```
unhexlify(b'48656c6c6f') => b'Hello'
```
