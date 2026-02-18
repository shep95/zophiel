import os
from cryptography.fernet import Fernet

class Vault:
    """
    MONAD VAULT - ELITE ENCRYPTION MODULE
    -------------------------------------
    Uses Fernet (AES-128 with HMAC) for symmetric encryption.
    """
    
    def __init__(self, key_path="monad_master.key"):
        self.key_path = key_path
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)

    def _load_or_generate_key(self):
        """Loads the master key or generates a new one if missing."""
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as key_file:
                key_file.write(key)
            print(f"[*] NEW MASTER KEY GENERATED: {self.key_path}")
            print(f"[*] WARNING: DO NOT LOSE THIS KEY. DATA WILL BE IRRECOVERABLE.")
            return key

    def encrypt_data(self, data: str) -> bytes:
        """Encrypts a string or bytes."""
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data)

    def decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypts bytes back to string."""
        return self.cipher.decrypt(encrypted_data).decode()

    def encrypt_file(self, file_path: str):
        """Encrypts a file in place (appends .enc)."""
        with open(file_path, "rb") as f:
            data = f.read()
        
        encrypted = self.cipher.encrypt(data)
        
        enc_path = file_path + ".enc"
        with open(enc_path, "wb") as f:
            f.write(encrypted)
            
        os.remove(file_path) # Secure delete original
        return enc_path

    def decrypt_file(self, enc_path: str):
        """Decrypts a .enc file."""
        if not enc_path.endswith(".enc"):
            raise ValueError("File must end with .enc")
            
        with open(enc_path, "rb") as f:
            data = f.read()
            
        decrypted = self.cipher.decrypt(data)
        
        orig_path = enc_path[:-4]
        with open(orig_path, "wb") as f:
            f.write(decrypted)
            
        return orig_path
