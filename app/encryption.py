from cryptography.fernet import Fernet
import os

KEY_PATH = os.path.join(os.path.dirname(__file__), '..', 'encryption_key.key')

def load_encryption_key():
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_PATH, 'wb') as f:
            f.write(key)
        return key

key = load_encryption_key()
cipher = Fernet(key)

def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()
