from Crypto.Cipher import AES
from getpass import getpass
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame , TimeFrameUnit
import time
from alpaca_trade_api.common import URL
from alpaca_trade_api.stream import Stream

def login():

    print("login")

def signup():
    username = input("username: ")
    while True:
        password = getpass("password: ")
        reconfirm = input("Re-enter password: ")
        if reconfirm == password:
            break
        else:
            print("password doesn't match")
    print(f'Hi there {username}, we just need your Key and s-Key')
    valid  = False
    while not valid:                    
        key = input("Key: ")
        skey = input("s-Key: ")
        valid  = validate(key, skey)
    plaintext = key + skey
    
    safe_content = encrypt(password, plaintext)
    write_file(username,password,safe_content)

    print('You are good to go!')

        



def validate(key,skey):
    try:
        api = tradeapi.REST(
            key_id= key,
            secret_key=skey,
            base_url='https://paper-api.alpaca.markets'
            )
        account = api.get_account()
        if account.status == 'ACTIVE':
            print('verified')
            return True
    except:
        print('Error your Key or Secret Key are wrong')
        return False



    
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

def write_file(username,password,safe_content):

    with open('keys.txt','a') as f:
        f.write(f'{username}|{password}|{key}|{skey}\n')


      
signup()