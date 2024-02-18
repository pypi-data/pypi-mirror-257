#/usr/bin/env python
_Author_ = "Sujit Mandal"
_Version_ = "1.0"

import base64
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# Encrypt the plain_text
def encrypt_plain_text(PLAIN_TEXT, LENGTH, TOKEN_BYTES, ITERATIONS):
    salt =  secrets.token_bytes(TOKEN_BYTES) 
    PLAIN_TEXT = PLAIN_TEXT.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=LENGTH,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(PLAIN_TEXT))


    fer_net = Fernet(key)
    encrypted_plain_text = fer_net.encrypt(PLAIN_TEXT)

    return(encrypted_plain_text, key)


# Decrypt the encrypted plain_text
def decrypt_plain_text(encrypted_plain_text, key):
    f = Fernet(key)
    decrypted_plain_text = f.decrypt(encrypted_plain_text)
    return decrypted_plain_text.decode()




if __name__ == '__main__':
    PLAIN_TEXT      = 'sujit' # plain text to be decrypted
    LENGTH          = 32      # length of hash  32/64/128/256 bytes
    ITERATIONS      = 100000  # number of iterations 100000
    TOKEN_BYTES     = 16      # 16 bytes (128 bits) is a common size for salts



    encrypted_plain_text, key = encrypt_plain_text(PLAIN_TEXT, LENGTH, TOKEN_BYTES, ITERATIONS)
    print("Encrypted plain_text:", encrypted_plain_text)
    print("Encrypted Key:", key)


    decrypted_plain_text = decrypt_plain_text(encrypted_plain_text, key)
    print("Decrypted plain_text:", decrypted_plain_text)