import zmq
import threading
import sys

isServer = False

def error():
    print("Error")
    quit()

context = zmq.Context()
pub = context.socket(zmq.PUB)
sub = context.socket(zmq.SUB)
if len(sys.argv) == 1:
    isServer = True
    print("binding server to ports 5555 and 5556")
    pub.bind("tcp://*:5555")
    sub.bind("tcp://*:5556")
    sub.setsockopt_string(zmq.SUBSCRIBE, "")
#elif len(sys.argv) == 2:
else:
    isServer = False
    print("Connecting to server at: " + sys.argv[1])
    pub.connect("tcp://" + sys.argv[1] + ":5556")
    sub.connect("tcp://" + sys.argv[1] + ":5555")
    sub.setsockopt_string(zmq.SUBSCRIBE, "")

if isServer:
    while True:
        message = input("> ")
        pub.send(message.encode())
        message = sub.recv().decode()
        print("them> ", message)

else:
    while True:
        message = sub.recv().decode()
        print("them> ", message)
        message = input("> ")
        pub.send(message.encode())




