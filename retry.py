from Crypto.Cipher import AES
from getpass import getpass

def login():
    print("login")

def signup():
    print("signup")

    
def encrypt(key,plaintext):

    #key is password

    iv = 'thiscanbeoverused'
    cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = cipher.encrypt(plaintext)

    return ciphertext

def decrypt(key,ciphertext):
    iv = 'thiscanbeoverused'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext