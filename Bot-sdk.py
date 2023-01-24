from Crypto.Cipher import AES #this is acting very wierd might have to replace
from getpass import getpass
import time
from alpaca.trading.client import TradingClient 


#      PKMS1S5M1C60839ET2QC 
#      YaXCd0ItTQUPwFwPcRECyQs71UnuPlqnHhPZFjWR

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
    #plaintext = key + skey
    #safe_content = encrypt(password, plaintext)
    write_file(username,password,key,skey)

    print('You are good to go!')

        



def validate(key,skey): 
    try:
        trading_client = TradingClient(key, skey)

        account = trading_client.get_account()
        return True
    except:
        print('Error your Key or Secret Key are wrong')
        return False



    
def encrypt(key,plaintext): #putting this function in the back for now

    #key is password

    iv = 'thiscanbeoverused'
    cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = cipher.encrypt(plaintext)

    return ciphertext

def decrypt(key,ciphertext): #putting this function in the back for now

    iv = 'thiscanbeoverused'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

def write_file(username,password,key,skey):


    with open('keys.txt','a') as f:
        f.write(f'{username}|{password}|{key}|{skey}\n')      


      
signup()