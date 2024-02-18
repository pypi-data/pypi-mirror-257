## text-encrypt-decrypt :
[![Downloads](https://static.pepy.tech/personalized-badge/text-encrypt-decrypt?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/text-encrypt-decrypt)[![GitHub license](https://img.shields.io/github/license/sujitmandal/text-encrypt-decrypt)](https://github.com/sujitmandal/text-encrypt-decrypt/blob/master/LICENSE) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/text-encrypt-decrypt) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/text-encrypt-decrypt) ![PyPI](https://img.shields.io/pypi/v/text-encrypt-decrypt) 


```
plain text encrypt decrypt

plain text encryption and decryption with SHA256 algorithm.
```


## Package Installation : 
```
pip install text-encrypt-decrypt
```
[Pypi Package Link](https://pypi.org/project/text-encrypt-decrypt/)


## How to import the module:
```python
PLAIN_TEXT      = 'sujit' # plain text
LENGTH          = 32      # length of hash 
ITERATIONS      = 100000  # number of iterations
TOKEN_BYTES     = 16      # 16 bytes (128 bits) is a common size for salts
```
## Plain Text Encrypt : 
```python
from text_encrypt_decrypt.text_encrypt_decrypt import encrypt_plain_text

encrypted_plain_text, key = encrypt_plain_text(PLAIN_TEXT, LENGTH, TOKEN_BYTES, ITERATIONS)

print("Encrypted plain_text:", encrypted_plain_text)

print("Encrypted Key:", key)
```

## Decrypt Encrypted Plain Text : 
```python
from text_encrypt_decrypt.text_encrypt_decrypt import decrypt_plain_text

decrypted_plain_text = decrypt_plain_text(encrypted_plain_text, key)

print("Decrypted plain_text:", decrypted_plain_text)
```


## Required package’s:
```
• pip install cryptography
```
## License:
MIT Licensed

## Author:
Sujit Mandal

[GitHub](https://github.com/sujitmandal)

[PyPi](https://pypi.org/user/sujitmandal/)

[LinkedIn](https://www.linkedin.com/in/sujit-mandal-91215013a/)
