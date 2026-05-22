from utilities.crypto_util import CryptoUtil

# Encrypt
encrypted = CryptoUtil.encrypt("admin")

print("Encrypted:")
print(encrypted)

# Decrypt
decrypted = CryptoUtil.decrypt(encrypted)

print("\nDecrypted:")
print(decrypted)