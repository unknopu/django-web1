import os, binascii, hashlib, Crypto, base64
from string import ascii_lowercase, ascii_uppercase
from random import randint
from Crypto.Cipher import PKCS1_OAEP, AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse
from base64 import b64encode, b64decode
from hashlib import sha512

mySECRET = "enc secret"

class myRSA():
    def __init__(self):
        self.private_key = os.getcwd() + "/bankservice/rsa_private.pem"
        self.public_key = os.getcwd() + "/bankservice/rsa_public.pem"
        # self.private_key = os.getcwd() + "/rsa_private.pem"
        # self.public_key = os.getcwd() + "/rsa_public.pem"
        
    def encrypt(self, data: str) -> str:
        msg = data.encode()
        key = RSA.importKey(open(self.public_key, 'rb').read())
        pubKey = key.publickey()
        
        encryptor = PKCS1_OAEP.new(pubKey)
        encrypted = encryptor.encrypt(msg)
        ciphertext = binascii.b2a_hex(encrypted).decode()
        return ciphertext


    def decrypt(self, ciphertext: str) -> str:
        ciphertext = base64.standard_b64decode(ciphertext)
        bank_private_key = RSA.import_key(open(self.private_key).read())
        cipher = PKCS1_v1_5.new(bank_private_key)
        pt = cipher.decrypt(ciphertext, None)
        return pt
    
    def get_publicKey(self):
        key = RSA.importKey(open(self.public_key, 'rb').read())
        pubKey = key.publickey()
        return key.export_key()
        
    def get_privteKey(self):
        key = RSA.importKey(open(self.private_key, 'rb').read())
        d, n = key.d, key.n
        return d, n
        
class myAES:
    def __init__(self, key: str):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def add_padding(self, plain_text):
        bytes2pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(bytes2pad)
        padding_string = ascii_string * bytes2pad
        return plain_text+padding_string

    def remove_padding(self, txt):
        last_character = txt[len(txt) - 1:]
        return txt[:-ord(last_character)]
    
    def encrypt(self, plaintext) -> str:
        plaintext = self.add_padding(plaintext)
        iv = Crypto.Random.new().read(self.block_size)
        encryptor = AES.new(self.key, AES.MODE_CBC, iv)
        ciphertext = encryptor.encrypt(plaintext.encode())
        return b64encode(iv+ciphertext).decode('utf-8')

    def decrypt(self, ciphertext, key=None) -> str:
        ciphertext = b64decode(ciphertext)
        iv = ciphertext[:self.block_size]
        if key != None:
            decryptor = AES.new(key, AES.MODE_CBC, iv)
        else:
            decryptor = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = decryptor.decrypt(ciphertext[self.block_size:]).decode('utf-8')
        return self.remove_padding(plain_text)

class myOTP:
    def __init__(self) -> None:
        self.ALPHABET = ascii_uppercase + " +" + ascii_lowercase
        
    def random_sequence(self, plaintext):
        random_sequence = []
        # Generateing as many random values as the number of character in the plain text
        # size of the key is equal to size of the plain text
        for rand in range(len(plaintext)):
            random_sequence.append(randint(0, len(self.ALPHABET)))
        return random_sequence

    def encrypt(self, plaintext, key=None):
        plaintext = "slat+" + plaintext + "+salt"
        print(f'{plaintext = }')
        if(key == None):
            key = self.random_sequence(plaintext)
        cipher_text = ''
        # Consider all the plain text letters: enumberation
        for index, char in enumerate(plaintext):
            key_index = key[index]
            char_index = self.ALPHABET.find(char)
            cipher_text += self.ALPHABET[(char_index+key_index)%len(self.ALPHABET)]
        return cipher_text, key

    def decrypt(self, ciphertext, key):
        plaintext = ''
        for index, char in enumerate(ciphertext):
            key_index = key[index]
            # print(key_index)
            char_index = self.ALPHABET.find(char)
            # print(char_index)
            print((char_index-key_index)%len(self.ALPHABET))
            
            plaintext += self.ALPHABET[(char_index-key_index)%len(self.ALPHABET)]
        return plaintext.split("+")[1]

def TEST_OTP():
    msg = "testinG mY onE timE paD."
    otp = myOTP()
    random_seq = otp.random_sequence(msg)
    ct, key = otp.encrypt(msg)
    pt = otp.decrypt(ct, key)
    print("===================random_seq===================")
    print(random_seq)
    print("===================cipher text===================")
    print(ct, len(ct))
    print("===================plain text===================")
    print(pt, len(pt))
    
def TEST_RSA():
    rsa = myRSA()
    # hash_password = hashlib.sha512("this is my secret".encode()).hexdigest()
    cipher = rsa.encrypt("hash_password")
    pt = rsa.decrypt(cipher)
    print("===================hash password===================")
    print(cipher)
    print("===================encrypted===================")
    print(cipher)
    print("===================decrypted===================")
    print(pt)
    
def TEST_AES():
    key = "this is my secret111"
    msg = "encrypt this message pls!"
    aes = myAES(key)
    cipher = aes.encrypt(msg)
    pt = aes.decrypt(cipher)
    print(f'cipher text({type(cipher)}) = {cipher}')
    print(f'plain text({type(pt)}) = {pt} \n')
    return cipher

def TEST_GETKEY():
    mykey = myRSA()
    e, n = mykey.get_publicKey()
    print("=================pubkey=================\n",e,"\n",n)
    
    d, n = mykey.get_privteKey()
    print("=================privkey=================\n",d,"\n",n)

# e = '0x10001'
# n = '0xb7b9e1e94931a14b64fb088d25215d3d34f7aaf042b54a904e2f29864faa63a2bb9097fc6e9748717a1ed6fab4341352438ea89b8c5c35009278f35ee08b36324ab4e79295fe0f589df13277d350ef9e05c1d462f0d78e1986589f91c987889dfc0f26feedfd1be1db17ac1cde450a90a1b4384d40fb7a2adac42e5ecf6f7b57'
# d = '0x4b4a70aaf264d54d99574a9cd4ef844f35ea9cf192d4ca76b2a39f27bc73fe1acd34a7243a89e295264f8717fc4b2ef3d25d9ef9079f2dd54b3127c2e4d007e808009cc53ee06b464ba547b29481d4a765af1518b44d0af9cae450562d7726e1d5534dc58a8e55dc5725d851b0c043a24096306f4eed64554638a033e5c69949'

def myNewPersonalKey():
    keyPair = RSA.generate(bits=1024)
    # e, n, d = int(e, 16), int(n, 16), int(d, 16)
    return hex(keyPair.e), hex(keyPair.n), hex(keyPair.d)

# enc = myOTP()
# ct = "GsLJIqegrxFFmBY+aCUSe"
# key = [14, 7, 37, 16, 35, 9, 0, 49, 6, 9, 33, 9, 52, 10, 39, 50, 1, 10, 46, 33, 39]
# pt = enc.decrypt(ct, key)
# print("===============================")
# print(pt)

# data = '+'.join([str(i) for i in key])
# print("===============================")
# print(ascii_uppercase + " +" + ascii_lowercase)




# b64_ciphertext = "bbo/bDWFXsLmHpqRcMtzw01taQMUWdoH0v9vlQJBFuvIzFpuVM66Zgj46Qo2rAJsr1SksqwBeQY2yVx8nVYNxKfVe8Q/RcDrBwz1kJEtjsFqQDjKyzu65AY75TXogX4vm5klR3Mny90kphWwAufbXU3ulVZ05wi0s4kMNUo/axCkzK0HzVl3tKJ2GwEI0vEMlY8mXI8foqBti6zuc/80K+P7aPgC43Wq6OKSXfMvDVqiHRpS6w+RyW8Lzjq66WOmxBZN3NyIWcwa8GZnrrx1RsLLzVA+6JPfyxx9GWN1WUWel4hByK8JkAfrmtF+QBk8GnqNrL2kqSShVvXmMQCwsw=="
# rsa = myRSA()
# print("===============================")
# pt = rsa.decrypt(b64_ciphertext)
# print(pt)