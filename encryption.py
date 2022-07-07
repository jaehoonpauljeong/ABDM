
import base64
from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Cipher import DES
from Cryptodome.Cipher import DES3



class AESCipher:
    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw.encode('utf-8') ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

class DESCipher:
    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( DES.block_size )
        cipher = DES.new( self.key, DES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw.encode('utf-8') ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:8]
        cipher = DES.new(self.key, DES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[8:] ))

class TripleDESCipher:
    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( DES3.block_size )
        cipher = DES3.new( self.key, DES3.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw.encode('utf-8') ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:8]
        cipher = DES3.new(self.key, DES3.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[8:] ))

BS = 16
pad = lambda s: s + (BS - len(s.encode('utf-8')) % BS) * chr(BS - len(s.encode('utf-8')) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

data_size = 1024
# with open("huino/healthcare_data_" + str(data_size) + ".txt", "r") as f:
#     sensitive_data = f.readline()
