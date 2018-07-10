from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol import KDF

class crypto:
    def __init__(self,pwd):
        self.pwd = pwd

    def encrypt(self, data):
        salt = get_random_bytes(8)
        key = KDF.PBKDF2(self.pwd, salt) #128bit key derivation function
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        return salt + iv + cipher.encrypt(data)

    def decrypt(self,msg):
        key = KDF.PBKDF2(self.pwd, msg[:8])
        cipher = AES.new(key, AES.MODE_CFB, msg[8:24])
        return cipher.decrypt(msg[24:])


if __name__ == "__main__":
    c = crypto('Gbmktzqh1')
    encrypt_data = c.encrypt('doxuanquy'.encode())
    print(encrypt_data)
    print(c.decrypt(encrypt_data))