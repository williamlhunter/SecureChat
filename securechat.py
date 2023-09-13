import zmq
import threading
import sys

isServer = False

def error():
    print("Error")
    quit()

context = zmq.Context()
if len(sys.argv) == 1:
    isServer = True
    print("Binding server to port 5555")
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")
#elif len(sys.argv) == 2:
else:
    isServer = False
    print("Connecting to server at: " + sys.argv[1])
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://" + sys.argv[1] + ":5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

if isServer:
    while True:
        message = input("> ")
        socket.send(message.encode())

else:
    while True:
        message = socket.recv().decode()
        print("them> ", message)




