import base64
import hashlib
from cryptography.fernet import Fernet

class CryptoUtil:

    # Secret passphrase
    PASSPHRASE = "Sec@Mark#22_05_26$_Aml_PW"

    @staticmethod
    def _generate_key():
        """
        Generates a Fernet-compatible key from passphrase
        """
        key = hashlib.sha256(
            CryptoUtil.PASSPHRASE.encode()
        ).digest()

        return base64.urlsafe_b64encode(key)

    @staticmethod
    def encrypt(text):
        """
        Encrypt plain text
        """
        key = CryptoUtil._generate_key()
        cipher = Fernet(key)

        encrypted_text = cipher.encrypt(text.encode())

        return encrypted_text.decode()

    @staticmethod
    def decrypt(encrypted_text):
        """
        Decrypt encrypted text
        """
        key = CryptoUtil._generate_key()
        cipher = Fernet(key)

        decrypted_text = cipher.decrypt(
            encrypted_text.encode()
        ).decode()

        return decrypted_text