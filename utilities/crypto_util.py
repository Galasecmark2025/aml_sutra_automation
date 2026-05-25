# import base64
# import hashlib
# from cryptography.fernet import Fernet

# class CryptoUtil:

#     # Secret passphrase
#     PASSPHRASE = "Sec@Mark#22_05_26$_Aml_PW"

#     @staticmethod
#     def _generate_key():
#         """
#         Generates a Fernet-compatible key from passphrase
#         """
#         key = hashlib.sha256(
#             CryptoUtil.PASSPHRASE.encode()
#         ).digest()

#         return base64.urlsafe_b64encode(key)

#     @staticmethod
#     def encrypt(text):
#         """
#         Encrypt plain text
#         """
#         key = CryptoUtil._generate_key()
#         cipher = Fernet(key)

#         encrypted_text = cipher.encrypt(text.encode())

#         return encrypted_text.decode()

#     @staticmethod
#     def decrypt(encrypted_text):
#         """
#         Decrypt encrypted text
#         """
#         key = CryptoUtil._generate_key()
#         cipher = Fernet(key)

#         decrypted_text = cipher.decrypt(
#             encrypted_text.encode()
#         ).decode()

#         return decrypted_text

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class CryptoUtil:

    PASSPHRASE = "Sec@Mark#220526$_Aml_PW"

    # 16-byte IV
    IV = b'1234567890123456'

    @staticmethod
    def _get_key():
        return hashlib.sha256(
            CryptoUtil.PASSPHRASE.encode()
        ).digest()

    @staticmethod
    def encrypt(text):

        key = CryptoUtil._get_key()

        cipher = AES.new(
            key,
            AES.MODE_CBC,
            CryptoUtil.IV
        )

        encrypted_bytes = cipher.encrypt(
            pad(text.encode(), AES.block_size)
        )

        return base64.b64encode(
            encrypted_bytes
        ).decode()

    @staticmethod
    def decrypt(encrypted_text):

        key = CryptoUtil._get_key()

        encrypted_bytes = base64.b64decode(
            encrypted_text
        )

        cipher = AES.new(
            key,
            AES.MODE_CBC,
            CryptoUtil.IV
        )

        decrypted = unpad(
            cipher.decrypt(encrypted_bytes),
            AES.block_size
        )

        return decrypted.decode()