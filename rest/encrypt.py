from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Protocol import KDF


def gen_key_pair(**kwargs):
    """
    Gen pair of public and private key
    """
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return (public_key, private_key)

def encrypt(pwd, data):
    salt = get_random_bytes(8)
    key = KDF.PBKDF2(pwd, salt) #128bit key derivation function
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return salt + iv + cipher.encrypt(data)

def decrypt(pwd, msg):
    key = KDF.PBKDF2(pwd, msg[:8])
    cipher = AES.new(key, AES.MODE_CFB, msg[8:24])
    return cipher.decrypt(msg[24:])

def encrypt_RSA(public_key, data):
    file_out = open("encrypted_data.bin", "wb")
    recipient_key = RSA.import_key(public_key)
    session_key = get_random_bytes(16)
    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)
    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data.encode())
    [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]

def decrypt_RSA(private_key):
    private_key = RSA.import_key(private_key)
    file_in = open("encrypted_data.bin", "rb")
    enc_session_key, nonce, tag, ciphertext = \
        [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    print(data.decode("utf-8"))
    
if __name__ == "__main__":
    public_key, private_key = gen_key_pair()
    data = "doxuanquy"
    encrypt_RSA(public_key, data)
    decrypt_RSA(private_key)