from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from threading import Thread
from time import sleep
import zmq
import sys

def sub_routine(socket, crypto):
    while True:
        cipherText = socket.recv()
        print("recieved ciphertext: ", cipherText)
        message = crypto.update(cipherText).decode()
        print("them> ", message)

context = zmq.Context()
pub = context.socket(zmq.PUB)
sub = context.socket(zmq.SUB)


#Are we running as a server?
if len(sys.argv) == 1:
    isServer = True
    pub.bind("tcp://*:5555")
    sub.bind("tcp://*:5556")
else:
    isServer = False
    pub.connect("tcp://" + sys.argv[1] + ":5556")
    sub.connect("tcp://" + sys.argv[1] + ":5555")

sub.setsockopt_string(zmq.SUBSCRIBE, "")

#handshake
if isServer:
    message = sub.recv().decode()
    if message != "hello":
        raise Exception("handshake failed")
else:
    #sleep resolves a cursed timing issue
    sleep(0.1)
    pub.send(b"hello")

#Diffie-Hellman
privateKey = x25519.X25519PrivateKey.generate()
publicKey = privateKey.public_key().public_bytes_raw()
pub.send(publicKey)
theirPublicKey = x25519.X25519PublicKey.from_public_bytes(sub.recv())
sharedKey = privateKey.exchange(theirPublicKey)
print(len(sharedKey))
keyIv = HKDF(
    algorithm=hashes.SHA256(),
    length=48,
    salt=None,
    info=b'handshake data',
).derive(sharedKey)
key = keyIv[:32]
iv = keyIv[-16:]

#initalize AES
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
encryptor = cipher.encryptor()
decryptor = cipher.decryptor()

#start listenting thread
subber = Thread(target=sub_routine, args=[sub, decryptor])
subber.start()

#prompt for messages
while True:
    message = input("> ")
    for i in range(16 - len(message) % 16):
        message += '\0'
    cipherText = encryptor.update(message.encode())
    print("outgoing ciphertext: ", cipherText)
    pub.send(cipherText)
