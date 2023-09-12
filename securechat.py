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
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
elif len(sys.argv) == 2:
    isServer = False
    print("Connecting to server at: " + sys.argv[1])
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://" + sys.argv[1] + ":5555")

if isServer:
    while True:
        message = input("> ")
        socket.send(message)

else:
    while True:
        message = socket.recv()
        print("them: %s" % message)




