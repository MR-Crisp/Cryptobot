import bcrypt #to do the hashing for the password so the user can be authenticated
import alpaca_trade_api as tradeapi
from getpass import *
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad , unpad


def auth():
    confirm = int(input('1 For new profile \n2 For existing profile \nenter here:   '))
    if confirm == 1:
        name_found = True
        while name_found == True:
            name = input('Enter your new username')
            name_found = False
            with open('keys.txt','r', encoding = 'utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    pos = line.split('|')
                    if pos[0] == name:
                        print('Username is Taken')
            veri = False
            while not veri:
                key = input('Enter your public Key here :')
                sec_key = getpass('Enter your secret Key, (No one will be able to see this!)')
            
                try:        # if the api submits an error, this allows for the user to fix it
                    api = tradeapi.REST(
                        key_id= key,
                        secret_key=sec_key,
                        base_url='https://paper-api.alpaca.markets'
                    )
                    account = api.get_account()
                    if account.status == 'ACTIVE':
                        veri = True
                        print('verified')
                        
                        password = getpass('Enter your new password(And make sure no to forget it!)')
                        
                        data = name+'|'+key+'|'+sec_key+'|'
                        data = bytes(data, 'utf-8')
    
                        
    
                        hash_pass = hashed(password)
                        
                    
                        encrypted = str(encryption(password,data))
                        
    
    
                        with open('keys.txt','a', encoding = 'utf-8') as f: #adds details to file
                            f.write(encrypted)
                            f.write('|')
                            f.write(hash_pass)
                            f.write('\n')

                except:            
                    print('Error your Key or Secret Key are wrong')


    elif confirm == 2:
        username = input('enter username')
        password = input('Enter your password').encode('utf-8') 
    
        passchecker = hash_compare(password)
        print(passchecker)
        if passchecker[0]:

            details = decryption(password,passchecker[1]) #gives the the details in the form of a list 0 is username, 1 is key, 2 is secret key and 3 is password

            if username == details[1]:
                print(f'You have looged in {username}!')
                
                api = tradeapi.REST(
                    key_id=details[1],
                    secret_key=details[2],
                    base_url='https://paper-api.alpaca.markets'
                )
    
                return api

        else:
            print('Username or password has not matched, try again:')
            return auth()



def encryption(password,data):
    salt = b'\xa4\xdc\x9c\xdd\xdeS^N\\\xf4/U\xdbG5I\xdf\xa7\x9e\xc3\xa5\xf4\x8e\x0e\xa2\xac\x01L2@\xaf-'
    key = PBKDF2(password,salt,dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted = cipher.encrypt(pad(data,AES.block_size))
    return encrypted

    

def stock(tradetype,api):
    try:    
        order = api.submit_order(
            symbol='BTC/USD',
            qty=1,
            type='market',
            side=tradetype,        
            time_in_force='ioc',) #has to be immediate or killed (ioc), so that the order either happens or it doesnt
    except:
        print('Error Something went wrong')


def hashed(password):
    temp_pass = bytes(password, 'utf-8')
    hash_pass = bcrypt.hashpw(temp_pass, bcrypt.gensalt()) # hashes password so it can be checked with later
    return hash_pass

def hash_compare(password):
    with open('keys.txt','r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            pos = line.split('|')              
            hashed = bytes(pos[1].strip(),'utf-8')
            if bcrypt.checkpw(password, hashed):
                print('match') # works  only have to refine it now
                print(line)
                returning = [True,line]
                return returning
            else:
                print('failed') # password  fin and now i have to code in username check
    
    return False


def decryption(password,content):
    content = content.strip()
    print(content)
    details = password.decrypt(content,'utf-8') # working on this something isnt right i think it might be the \n but idk...
    pos = details.split('|')
    return pos
                 



api = auth()

