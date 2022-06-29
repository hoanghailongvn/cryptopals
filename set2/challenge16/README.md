# **[set 2 - challenge 16](https://cryptopals.com/sets/2/challenges/16): CBC bitflipping attacks**


## Đề bài
Như challenge13, ta cũng thay đổi ciphertext để khi decrypt sẽ được plaintext như mong muốn mà nếu nhập trực tiếp sẽ không được: ";admin=true"

## Code
Implement một số hàm cần thiết cho challenge16:
- padding: pkcs7, pkcs7_unpadding
- encrypt, decrypt bằng mode cbc như đề bài
- check is_admin
```
from Crypto.Cipher import AES
from random import randint

def random_bytes(length: int) -> bytes:
    ret = []
    for _ in range(length):
        ret.append(randint(0, 255))
    
    return bytes(ret)

def pkcs7(message: bytes, blocksize: int) -> bytes:
    diff = blocksize - len(message) % blocksize

    padding = bytes([diff]*diff)

    ret = message + padding
    return ret

def pkcs7_unpadding(message:bytes) -> bytes:
    pad = message[-1]
    return message[: -pad]

blocksize = 16
consistent_but_unknown_key = random_bytes(16)
consistent_but_unknown_iv = random_bytes(blocksize)

def challenge16_encrypt(attacker_controlled: bytes):
    plaintext = b"comment1=cooking%20MCs;userdata=" + attacker_controlled.replace(b'=', b'').replace(b';', b'') + b";comment2=%20like%20a%20pound%20of%20bacon"
    plaintext = pkcs7(plaintext, blocksize)

    cryptor = AES.new(consistent_but_unknown_key, AES.MODE_CBC, consistent_but_unknown_iv)
    ciphertext = cryptor.encrypt(plaintext)

    return ciphertext

def challenge16_decrypt(ciphertext: bytes):
    cryptor = AES.new(consistent_but_unknown_key, AES.MODE_CBC, consistent_but_unknown_iv)
    plaintext = cryptor.decrypt(ciphertext)
    plaintext = pkcs7_unpadding(plaintext)

    return plaintext

def is_admin(plaintext: bytes):
    return b'admin=true' in plaintext
```

## Ý tưởng
Nhìn lại sơ đồ decrypt của CBC mode

<img src="pictures/CBC_d.png">

Với prepend text và append text có sẵn, plaintext chia thành các block sẽ như sau:
```
0: comment1=cooking
1: %20MCs;userdata=
2: [attacker.......
3: .....controlled]
4: ;comment2=%20lik
5: e%20a%20pound%20
```
Quan sát block ciphertext thứ 2 đến khi được decrypt thành block plaintext thứ 2:
- đầu tiên sẽ đi qua decryption
- sau đó xor với block ciphertext thứ 1

Ta không biết key nên không động được vô bước decryption, nhưng ta có thể thay đổi block ciphertext thứ 1 => có thể thay đổi plaintext sau khi decryption tùy ý.

Để không làm thay đổi prepend text ở block ciphertext thứ 1. ta thay đổi mục tiêu như sau:
- đặt ";admin=true" ở block4
```
0: comment1=cooking
1: %20MCs;userdata=
2: rác.............
3: .....;admin=true
4: ;comment2=%20lik
5: e%20a%20pound%20
```
Như thế này thì khi thay đổi block ciphertext thứ 2, sẽ không ảnh hưởng đến prepend text.

## Solution
Tạo `attacker_controlled` = 32 ký tự 'a', các block plaintext sẽ trông như sau:
- plaintext0 = block plaintext thứ 0
```
plaintext0: b'comment1=cooking'
plaintext1: b'%20MCs;userdata='
plaintext2: b'aaaaaaaaaaaaaaaa'
plaintext3: b'aaaaaaaaaaaaaaaa'
plaintext4: b';comment2=%20lik'
plaintext5: b'e%20a%20pound%20'
plaintext6: b'of%20bacon\x06\x06\x06\x06\x06\x06'
```
Còn đây là các block ciphertext tương ứng:
- ciphertext0 = block ciphertext thứ 0
```
ciphertext0: b'\xa8\x1c\x8c\xf39\x17\xaeN\x99\xce\xfc\x1c\x9aJ\xc6l'
ciphertext1: b'\x93\xc4\xb3\xb6\x949{\x02z>\x931\xc2\xc4\xc1\xa9'
ciphertext2: b'\xc8\xdaN\xff\x89\xc3N]\xea\xf7\xd3\x93O\xd1\x8cB'
ciphertext3: b'\xcb\xd7\xd3\x0b\x97\xec96\xdb\x96\x1f\xbc\x0e\x80\xc2D'
ciphertext4: b'\x1bj\xc6V\x94.\x82k\x13\x84\xcc\xf0\xbd\xa5\x0e\x1c'
ciphertext5: b'2y\x1b\x8d`\x14\xb7C*\xb2$e\x16\xd0\x1c['
ciphertext6: b'\xe1\xf3\xfeb\xc5>\xe4\xd3\x85`\xb9v\xda\x82-\xaf'
```
ciphertext3 -> plaintext3 gồm 2 bước:
- decrypt ciphertext3 bằng aes: gọi kết quả là `temp`
- xor `temp` với ciphertext2 ra plaintext3

=>:
- `temp` = plaintext3 xor ciphertext2
- xor `temp` với string ".....;admin=true", kết quả thay vào ciphertext2
=> Khi decrypt sẽ ra ";admin=true"

Python code:
```
def crack():
    attacker_controlled = bytes('a'*32, 'ascii')

    ciphertext = challenge16_encrypt(attacker_controlled)
    #Chia thành từng block 16 bytes, cho vào list
    ciphertext_block16 = [ciphertext[i:i+blocksize] for i in range(0, len(ciphertext), blocksize)]

    # plaintext3 xor ciphertext2
    temp = stream_xor(bytes('a'*16, 'ascii'), ciphertext_block16[2])
    # change ciphertext2
    fake_ciphertext_block16 = ciphertext_block16
    fake_ciphertext_block16[2] = stream_xor(temp, b".....;admin=true")

    fake_ciphertext = b''.join(fake_ciphertext_block16)
    fake_plaintext = challenge16_decrypt(fake_ciphertext)

    print(fake_plaintext)
    print(is_admin(fake_plaintext))
```
Kết quả:
```
b'comment1=cooking%20MCs;userdata=\x97&\x06PX\x83\xc6-\xf22\xa8\xff"\xe1\xa6\xb2.....;admin=true;comment2=%20like%20a%20pound%20of%20bacon'
True
```
## References
