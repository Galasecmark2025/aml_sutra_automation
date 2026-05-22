from crypto_util import CryptoUtil

# Encrypt
encrypted = CryptoUtil.encrypt("MyPassword123")

print("Encrypted:")
print(encrypted)

# Decrypt
decrypted = CryptoUtil.decrypt(encrypted)

print("\nDecrypted:")
print(decrypted)