# **[set 2 - challenge 13](https://cryptopals.com/sets/2/challenges/13): ECB cut-and-paste**

## Đề bài

Để hiểu đề bài hơn, ta hãy nghĩ đến luồng hoạt động của server đối với cookie:
- 1. đọc email của user
- 2. tạo một đoạn cookie như là: `email=foo@bar.com&uid=10&role=user`
- 3. encrypt đoạn cookie này và gửi cho người dùng
- 4. mỗi khi user quay trở lại, server đọc đoạn encrypted cookie để xác định người dùng

Trong đó:
- có hai hàm chuyển đổi qua lại giữa cookie dạng string:
    ```
    email=foo@bar.com&uid=10&role=user
    ```
    và dạng dict
    ```
    {
    'email': foo@bar.com,
    'uid': 10
    'role: 'user'
    }
    ```
- hàm profile_for() nhận vào email và chuyển thành cookie dạng string, email không được có ký tự nguy hiểm '&' và '=' để không bị parse sai
- hàm encrypt và decrypt bằng aes ecb

## Mục tiêu
Tự tạo ra encrypted cookie mà khi server đọc được sẽ tạo ra profile có quyền `admin`

## Các hàm cần thiết
- cookie2dict: phân tích cookie 
    - lambda tạo ra anonymous functions: đọc thêm [tại đây](https://julien.danjou.info/python-functional-programming-lambda/)
    - map() thực thi hàm lambda với từng item. Ví dụ như đoạn code dưới đây, từng item của `s.strip('&').split('&')` sẽ được pass vào `lambda x: x.split('=')`
    ```
    def cookie2dict(s: str) -> dict:
        return dict(map(lambda x: x.split('='), s.strip('&').split('&')))
    ```
- dict2cookie: 
    ```
    def dict2cookie(d: dict) -> str:
        return '&'.join(map('='.join, d.items()))
    ```
- profile_for:
    - 1. produce dict
    - 2. from dict encode to cookie
    ```
    def profile_for(email: str):
        return dict2cookie({
            'email': email.replace('&', '').replace('=', ''),
            'uid': str(10),
            'role': 'user'
        })
    ```
- encrypt:
    ```
    def AES_encrypt(encoded_cookie):
        cryptor = AES.new(consistent_but_unknown_key, AES.MODE_ECB)
        ciphertext = cryptor.encrypt(pkcs7(encoded_cookie, blocksize))
        return ciphertext
    ```

- decrypt:
    ```
    def AES_decrypt_and_parse(encrypted_cookie: bytes) -> dict:
        cryptor = AES.new(consistent_but_unknown_key, AES.MODE_ECB)
        encoded_cookie = pkcs7_unpadding(cryptor.decrypt(encrypted_cookie))

        return cookie2dict(encoded_cookie.decode())
    ```

- recv_encrypted_cookie_for:
    - Ghép từng bước lại từ khi nhận được email từ người dùng đến khi trả về encrypted cookie:
        - 1. tạo profile dạng dict cho email
        - 2. từ profile dạng dict phân tích thành cookie
        - 3. mã hóa cookie bằng AES và gửi cho người dùng
    ```
    def recv_encrypted_cookie_for(email: str) -> bytes:
        cookie = profile_for(email)
        encrypted_cookie = AES_encrypt(bytes(cookie, 'ascii'))
        return encrypted_cookie
    ```

## Trước khi bắt đầu
Những gì ta đã biết:
- cookies được mã hóa bằng aes ebc
- key cố định
- được pad bằng pkcs7
- blocksize là 16
- cookie trước khi encrypt có dạng: 'email=our@email.com&uid=10&role=user'

## Ý tưởng
Vẫn lỗi bảo mật cơ bản với ECB, tuy không biết key nhưng ta vẫn có thể có được ciphertext block tương ứng với plaintext block.

email chúng ta gửi lên server sẽ được đưa vào cookie sau đó encrypt, đoạn này gọi là `attacker_controlled`

Hàm encrypt sẽ nhận vào plaintext cookie: 'email=|attacker_controlled|&uid=10&role=user'

Tiếp theo:
- phân tích plaintext cookie thành từng block 16 ký tự
- thay đổi `attacker_controlled` hợp lý sao cho khi đổi chỗ các block trong cookie, có thể xuất hiện string 'role=admin'
- lấy encrypted cookie mà server gửi về, đảo vị trí các block như khi đảo plaintext

## solution
Nếu ta nhập vào email = 'aaaaaaaaaa' + 'admin' + '\x0b'*0x0b + 'aaa', plaintext có thể được phân tích như sau
```
block1 = 'email=aaaaaaaaaa'
block2 = 'admin' + '\x0b'*0x0b
block3 = 'aaa&uid=10&role=
block4 = 'user' + '\x0c'*0x0c
```
Trong đó:
- '\x0b'*0x0b là padding pkcs7 thủ công
- '\x0c'*0x0c là padding được pkcs7 server thêm vào

Mục đích ta muốn có các block như này là để khi đổi chỗ block 2 với block 4:
```
block1 = 'email=aaaaaaaaaa'
block4 = 'user' + '\x0c'*0x0c
block3 = 'aaa&uid=10&role=
block2 = 'admin' + '\x0b'*0x0b
```
- xuất hiện role=admin
- padding pkcs7 hợp lệ

Python code:
- gửi email = 'aaaaaaaaaa' + 'admin' + '\x0b'*0x0b + 'aaa' cho server
- nhận về encrypted cookie
- đảo block2 với block4
- server đọc cookie này sẽ tạo ra profile có role=admin
```
def crack():
    email = 'aaaaaaaaaa' + 'admin' + '\x0b'*0x0b + 'aaa'

    encrypted_cookie = recv_encrypted_cookie_for(email)
    # Chia encrypted_cookie thành các block 16 bytes rồi cho vào list
    encrypted_cookie_block16 = [encrypted_cookie[i:i+blocksize] for i in range(0, len(encrypted_cookie), blocksize)]

    fake_encrypted_cookie = encrypted_cookie_block16[0] + encrypted_cookie_block16[3] + \
                            encrypted_cookie_block16[2] + encrypted_cookie_block16[1]

    profile = AES_decrypt_and_parse(fake_encrypted_cookie)
    print(profile)
```
Kết quả:
```
{'email': 'aaaaaaaaaauser\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0caaa', 'uid': '10', 'role': 'admin'}
```
Source code: [here](./script.py)

## References
- writeup: https://bernardoamc.com/ecb-cut-paste-attack/
- lambda: https://julien.danjou.info/python-functional-programming-lambda/
- map(): https://www.w3schools.com/python/ref_func_map.asp