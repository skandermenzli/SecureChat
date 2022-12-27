
#from Crypto import
import rsa

public_key, private_key = rsa.newkeys(1024)
test = public_key.save_pkcs1("PEM")
x = rsa.PublicKey.load_pkcs1(test)
print(x)
print("hiii")
