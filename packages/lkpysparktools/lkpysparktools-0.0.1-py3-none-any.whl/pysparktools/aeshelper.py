from Crypto.Cipher import AES
from base64 import b64decode, b64encode
import os

class AESHelper():
    def __init__(self, block_size = 16, iv = bytes([0] * 16), aes_mode = AES.MODE_CBC):
        self.block_size = block_size
        self.iv = iv
        self.aes_mode = aes_mode
        
    def generate_key(self):
        return os.urandom(self.block_size)
    
    def generate_base64_key(self):
        return b64encode(self.generate_key()).decode()
        
    def pad(self, s):
        return s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size).encode('utf8')

        
    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]
    
    def encrypt_from_bytes_key(self, plain_text, key):
        plain_text = plain_text.encode('utf8')
        plain_text = self.pad(plain_text)
        cipher = AES.new(key, self.aes_mode, self.iv)
        return b64encode(cipher.encrypt(plain_text)).decode()

    def decrypt_from_bytes_key(self, cipher_text, key):
        cipher_text = b64decode(cipher_text)
        cipher = AES.new(key, self.aes_mode, self.iv)
        return self.unpad(cipher.decrypt(cipher_text)).decode()
    
    def encrypt_from_base64_key(self, plain_text, base64_key):
        return self.encrypt(plain_text, b64decode(base64_key))
    
    def decrypt_from_base64_key(self, cipher_text, base64_key):
        return self.decrypt(cipher_text, b64decode(base64_key))
    
    def encrypt(self, plain_text, key):
        if(len(key) == 44):
            return self.encrypt_from_base64_key(plain_text, key)
        else:
            return self.encrypt_from_bytes_key(plain_text, key)
        
    def decrypt(self, cipher_text, key):
        if(len(key) == 44):
            return self.decrypt_from_base64_key(cipher_text, key)
        else:
            return self.decrypt_from_bytes_key(cipher_text, key)